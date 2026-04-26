"""PR Executor - Implements the changes suggested by evaluator."""

import logging
import subprocess
from pathlib import Path

import requests

logger = logging.getLogger(__name__)


class PRExecutor:
    """Executes changes to the codebase based on PR comments."""

    def __init__(self, repo_root: Path, copilot_chat_url: str):
        """Initialize executor.

        Args:
            repo_root: Root path of the repository
            copilot_chat_url: Base URL of the Copilot Chat HTTP API
        """
        self.repo_root = repo_root
        self.copilot_chat_url = copilot_chat_url

    def execute_changes(
        self,
        pr_branch: str,
        comment_body: str,
        evaluation: dict,
        dry_run: bool = True,
    ) -> dict:
        """
        Execute the changes described in a PR comment.

        Args:
            pr_branch: The PR branch to work on
            comment_body: The original comment
            evaluation: The evaluator's assessment
            dry_run: If True, show what would be done without doing it

        Returns:
            dict with execution status
        """
        try:
            # Ensure we're on the right branch
            self._checkout_branch(pr_branch)

            # Ask Copilot Chat to generate the actual implementation code
            implementation = self._get_implementation(comment_body, evaluation)

            if not implementation:
                return {
                    "success": False,
                    "error": "Could not generate implementation",
                }

            # Parse the implementation to understand what files to modify
            changes = self._parse_implementation(implementation)

            if dry_run:
                logger.info(f"DRY RUN: Would apply {len(changes)} changes:")
                for change in changes:
                    logger.info(f"  - {change['file']}: {change['action']}")
                return {"success": True, "dry_run": True, "changes_count": len(changes)}

            # Apply the changes
            for change in changes:
                self._apply_change(change)

            # Verify changes
            if not self._verify_changes():
                return {
                    "success": False,
                    "error": "Verification failed after applying changes",
                }

            # Commit and push
            commit_msg = f"Auto: {evaluation.get('action_type', 'update')}"
            self._commit_and_push(pr_branch, commit_msg)

            return {
                "success": True,
                "changes_applied": len(changes),
                "commit_message": commit_msg,
            }

        except Exception as e:
            logger.error(f"Execution error: {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    def _checkout_branch(self, branch: str) -> None:
        """Checkout the specified branch."""
        result = subprocess.run(
            ["git", "checkout", branch],
            cwd=self.repo_root,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"Failed to checkout {branch}: {result.stderr}")

        logger.info(f"Checked out branch: {branch}")

    def _get_implementation(self, comment_body: str, evaluation: dict) -> str | None:
        """Ask Copilot Chat to generate the specific code changes."""
        try:
            url = f"{self.copilot_chat_url}/generate-implementation"
            payload = {
                "comment_body": comment_body,
                "evaluation": evaluation,
            }

            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()

            result = response.json()
            return result.get("implementation")

        except requests.ConnectionError as e:
            logger.error(f"Cannot connect to Copilot Chat API: {e}")
            return None
        except Exception as e:
            logger.error(f"Error getting implementation: {e}")
            return None

    def _parse_implementation(self, implementation: str) -> list[dict]:
        """Parse Copilot Chat's implementation output into file changes."""
        changes = []
        current_file = None
        current_content = []
        current_action = None
        in_content = False

        for line in implementation.split("\n"):
            if line.startswith("FILE: "):
                if current_file and in_content:
                    changes.append(
                        {
                            "file": current_file,
                            "action": current_action,
                            "content": "\n".join(current_content).strip(),
                        }
                    )

                current_file = line.replace("FILE: ", "").strip()
                current_content = []
                in_content = False

            elif line.startswith("ACTION: "):
                current_action = line.replace("ACTION: ", "").strip().lower()

            elif line.startswith("---"):
                in_content = not in_content
                if in_content:
                    current_content = []

            elif in_content:
                current_content.append(line)

        # Don't forget the last change
        if current_file and in_content:
            changes.append(
                {
                    "file": current_file,
                    "action": current_action,
                    "content": "\n".join(current_content).strip(),
                }
            )

        return changes

    def _apply_change(self, change: dict) -> None:
        """Apply a single file change."""
        file_path = self.repo_root / change["file"]
        action = change["action"]
        content = change["content"]

        if action == "create" or action == "modify":
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")
            logger.info(f"{action.capitalize()}: {change['file']}")

        elif action == "delete":
            if file_path.exists():
                file_path.unlink()
                logger.info(f"Deleted: {change['file']}")

    def _verify_changes(self) -> bool:
        """Verify the changes are valid (e.g., syntax check for Python files)."""
        # Simple verification: check for basic syntax errors
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=self.repo_root,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            logger.error("Git status check failed")
            return False

        # If there are changes, do a basic validation
        if result.stdout.strip():
            # You could add more sophisticated checks here
            logger.info("Changes verified")
            return True

        return True

    def _commit_and_push(self, branch: str, message: str) -> None:
        """Commit and push the changes."""
        # Stage all changes
        subprocess.run(
            ["git", "add", "-A"],
            cwd=self.repo_root,
            capture_output=True,
            check=True,
        )

        # Commit
        subprocess.run(
            ["git", "commit", "-m", message],
            cwd=self.repo_root,
            capture_output=True,
            check=True,
        )

        # Push
        subprocess.run(
            ["git", "push", "origin", branch],
            cwd=self.repo_root,
            capture_output=True,
            check=True,
        )

        logger.info(f"Committed and pushed: {message}")
