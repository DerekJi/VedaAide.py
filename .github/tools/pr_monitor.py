#!/usr/bin/env python3
"""PR Monitor Daemon - Main monitoring loop."""

import json
import logging
import signal
import sys
import time
from datetime import datetime, timezone

import requests
from config import (
    AUTO_COMMIT,
    AUTO_PUSH,
    COPILOT_CHAT_URL,
    GITHUB_OWNER,
    GITHUB_REPO,
    GITHUB_TOKEN,
    MONITOR_LOG_FILE,
    POLL_INTERVAL_SECONDS,
    PROCESSED_COMMENTS_FILE,
    REPO_ROOT,
    STATE_DIR,
    TRUSTED_USERS,
)
from pr_evaluator import CommentContext, PRCommentEvaluator
from pr_executor import PRExecutor

# Setup logging
STATE_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(MONITOR_LOG_FILE),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


class PRMonitor:
    """Main PR monitoring daemon."""

    def __init__(self):
        """Initialize the monitor."""
        self.evaluator = PRCommentEvaluator(COPILOT_CHAT_URL)
        self.executor = PRExecutor(REPO_ROOT, COPILOT_CHAT_URL)
        self.processed_comments = self._load_processed_comments()
        self.running = True

        # Signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)

    def _handle_shutdown(self, signum, frame):
        """Handle shutdown signal."""
        logger.info("Shutdown signal received, stopping monitor...")
        self.running = False

    def run(self):
        """Main monitoring loop."""
        logger.info(f"Starting PR Monitor (interval: {POLL_INTERVAL_SECONDS}s)")
        logger.info(f"Trusted users: {', '.join(TRUSTED_USERS)}")

        # Verify Copilot Chat API is reachable
        if not self._verify_copilot_chat_connection():
            logger.error(
                "Cannot connect to Copilot Chat API. "
                "Make sure the VS Code Extension is running on localhost:3456"
            )
            return

        while self.running:
            try:
                self._check_prs()
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}", exc_info=True)

            if self.running:
                logger.info(f"Sleeping for {POLL_INTERVAL_SECONDS}s...")
                time.sleep(POLL_INTERVAL_SECONDS)

        logger.info("PR Monitor stopped")

    def _check_prs(self):
        """Check all open PRs for comments."""
        logger.info("Checking PRs...")

        prs = self._get_open_prs()
        if not prs:
            logger.info("No open PRs found")
            return

        logger.info(f"Found {len(prs)} open PRs")

        for pr in prs:
            self._process_pr(pr)

    def _get_open_prs(self) -> list:
        """Fetch all open PRs from GitHub."""
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/pulls"

        try:
            response = requests.get(
                url,
                headers=headers,
                params={"state": "open", "per_page": 50},
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching PRs: {e}")
            return []

    def _process_pr(self, pr: dict):
        """Process a single PR and its comments."""
        pr_number = pr["number"]
        pr_title = pr["title"]
        pr_body = pr.get("body", "")
        pr_branch = pr["head"]["ref"]
        pr_author = pr["user"]["login"]

        logger.info(f"Processing PR #{pr_number}: {pr_title}")

        # Get related issue info if linked
        issue_info = self._get_linked_issue(pr)

        # Get all comments on this PR
        comments = self._get_pr_comments(pr_number)
        if not comments:
            logger.info(f"  No comments on PR #{pr_number}")
            return

        for comment in comments:
            self._process_comment(
                pr_number=pr_number,
                pr_title=pr_title,
                pr_body=pr_body,
                pr_branch=pr_branch,
                pr_author=pr_author,
                issue_info=issue_info,
                comment=comment,
            )

    def _get_linked_issue(self, pr: dict) -> dict:
        """Get information about linked issue if any."""
        body = pr.get("body", "")
        # Simple pattern: look for "Closes #123" or "Fixes #456"
        import re

        match = re.search(r"(?:Closes|Fixes|Resolves)\s+#(\d+)", body)
        if not match:
            return {}

        issue_number = int(match.group(1))
        issue = self._get_issue(issue_number)
        return issue if issue else {}

    def _get_issue(self, issue_number: int) -> dict:
        """Fetch an issue by number."""
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/issues/{issue_number}"

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching issue #{issue_number}: {e}")
            return {}

    def _get_pr_comments(self, pr_number: int) -> list:
        """Get all review comments on a PR."""
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        url = (
            f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/pulls/{pr_number}/comments"
        )

        try:
            response = requests.get(
                url,
                headers=headers,
                params={"per_page": 50},
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching comments for PR #{pr_number}: {e}")
            return []

    def _process_comment(
        self,
        pr_number: int,
        pr_title: str,
        pr_body: str,
        pr_branch: str,
        pr_author: str,
        issue_info: dict,
        comment: dict,
    ):
        """Process a single PR comment."""
        comment_id = str(comment["id"])
        comment_author = comment["user"]["login"]
        comment_body = comment["body"]

        # Skip if already processed
        if comment_id in self.processed_comments:
            logger.debug(f"  Comment {comment_id} already processed")
            return

        # Skip if not from trusted user
        if comment_author not in TRUSTED_USERS:
            logger.info(f"  Skipping comment from untrusted user: {comment_author}")
            self._mark_processed(comment_id)
            return

        logger.info(f"  Evaluating comment #{comment_id} by {comment_author}")

        # Build context for evaluator
        context = CommentContext(
            pr_number=pr_number,
            pr_title=pr_title,
            pr_body=pr_body,
            pr_branch=pr_branch,
            pr_author=pr_author,
            issue_number=issue_info.get("number"),
            issue_title=issue_info.get("title"),
            issue_body=issue_info.get("body"),
            comment_author=comment_author,
            comment_body=comment_body,
            comment_id=comment_id,
            repository=f"{GITHUB_OWNER}/{GITHUB_REPO}",
        )

        # Evaluate the comment
        evaluation = self.evaluator.evaluate(context)
        logger.info(
            f"    Evaluation: actionable={evaluation.get('is_actionable')} "
            f"confidence={evaluation.get('confidence')} "
            f"risk={evaluation.get('risk_level')}"
        )

        if not evaluation.get("is_actionable"):
            logger.info(f"    Not actionable: {evaluation.get('reason')}")
            self._mark_processed(comment_id)
            return

        # High confidence and low risk only
        confidence = evaluation.get("confidence", 0)
        risk = evaluation.get("risk_level", "high")

        if confidence < 0.7:
            logger.info(f"    Confidence too low ({confidence}), skipping")
            self._mark_processed(comment_id)
            return

        if risk == "high":
            logger.info(f"    Risk level too high ({risk}), skipping")
            self._mark_processed(comment_id)
            return

        # Execute the changes
        logger.info(f"    Executing changes for PR #{pr_number}...")
        result = self.executor.execute_changes(
            pr_branch=pr_branch,
            comment_body=comment_body,
            evaluation=evaluation,
            dry_run=not (AUTO_COMMIT and AUTO_PUSH),
        )

        if result.get("success"):
            logger.info("    ✓ Successfully executed changes")
            logger.info(f"      Result: {json.dumps(result)}")
        else:
            logger.error(f"    ✗ Execution failed: {result.get('error')}")

        self._mark_processed(comment_id)

    def _load_processed_comments(self) -> set:
        """Load the set of already-processed comment IDs."""
        if not PROCESSED_COMMENTS_FILE.exists():
            return set()

        try:
            with open(PROCESSED_COMMENTS_FILE, encoding="utf-8") as f:
                data = json.load(f)
                return set(data.get("processed", []))
        except Exception as e:
            logger.error(f"Error loading processed comments: {e}")
            return set()

    def _mark_processed(self, comment_id: str):
        """Mark a comment as processed."""
        self.processed_comments.add(comment_id)

        try:
            with open(PROCESSED_COMMENTS_FILE, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "processed": list(self.processed_comments),
                        "last_updated": datetime.now(timezone.utc).isoformat(),
                    },
                    f,
                    indent=2,
                )
        except Exception as e:
            logger.error(f"Error saving processed comments: {e}")

    def _verify_copilot_chat_connection(self) -> bool:
        """Verify that Copilot Chat API is reachable."""
        try:
            url = f"{COPILOT_CHAT_URL}/health"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            logger.info(f"✓ Connected to Copilot Chat API at {COPILOT_CHAT_URL}")
            return True
        except requests.RequestException as e:
            logger.error(f"Cannot reach Copilot Chat API at {COPILOT_CHAT_URL}: {e}")
            return False


def main():
    """Entry point."""
    # Validate configuration
    if not GITHUB_TOKEN:
        logger.error("GITHUB_TOKEN not set")
        sys.exit(1)

    if not CLAUDE_API_KEY:
        logger.error("CLAUDE_API_KEY not set")
        sys.exit(1)

    monitor = PRMonitor()
    monitor.run()


if __name__ == "__main__":
    main()
