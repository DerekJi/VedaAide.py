"""PR Comment Evaluator using VS Code Copilot Chat."""

import logging
from dataclasses import dataclass

import requests

logger = logging.getLogger(__name__)


@dataclass
class CommentContext:
    """Context information for evaluating a PR comment."""

    pr_number: int
    pr_title: str
    pr_body: str
    pr_branch: str
    pr_author: str
    issue_number: int | None
    issue_title: str | None
    issue_body: str | None
    comment_author: str
    comment_body: str
    comment_id: str
    repository: str


class PRCommentEvaluator:
    """Evaluates PR comments using VS Code Copilot Chat."""

    def __init__(self, copilot_chat_url: str):
        """Initialize evaluator with Copilot Chat endpoint.

        Args:
            copilot_chat_url: Base URL of the VS Code Copilot Chat HTTP API
                Example: "http://localhost:3456"
        """
        self.copilot_chat_url = copilot_chat_url

    def evaluate(self, context: CommentContext) -> dict:
        """
        Evaluate if a PR comment is a reasonable, actionable instruction.

        Returns:
            dict with keys:
                - is_actionable (bool): Whether the comment is a valid instruction
                - action_type (str): Type of action (e.g., "code_fix", "docs_update")
                - confidence (float): 0.0-1.0 confidence score
                - reason (str): Explanation of evaluation
                - suggested_changes (str): If actionable, what changes should be made
                - risk_level (str): "low", "medium", "high"
        """
        try:
            # Call Copilot Chat API via HTTP
            url = f"{self.copilot_chat_url}/evaluate"
            payload = {
                "pr_number": context.pr_number,
                "pr_title": context.pr_title,
                "pr_body": context.pr_body,
                "pr_branch": context.pr_branch,
                "pr_author": context.pr_author,
                "issue_number": context.issue_number,
                "issue_title": context.issue_title,
                "issue_body": context.issue_body,
                "comment_author": context.comment_author,
                "comment_body": context.comment_body,
                "repository": context.repository,
            }

            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()

            return response.json()

        except requests.ConnectionError as e:
            logger.error(f"Cannot connect to Copilot Chat API at {self.copilot_chat_url}: {e}")
            return {
                "is_actionable": False,
                "error": f"Cannot connect to Copilot Chat: {e}",
                "confidence": 0.0,
                "reason": "Connection error to Copilot Chat API",
            }
        except Exception as e:
            logger.error(f"Error evaluating comment {context.comment_id}: {e}")
            return {
                "is_actionable": False,
                "error": str(e),
                "confidence": 0.0,
                "reason": f"Evaluation failed: {e}",
            }

    def _ensure_response_format(self, response: dict) -> dict:
        """Ensure the response has all expected fields with defaults."""
        defaults = {
            "is_actionable": False,
            "action_type": "unknown",
            "confidence": 0.0,
            "reason": "",
            "suggested_changes": "",
            "risk_level": "medium",
            "safety_concerns": [],
            "requires_manual_review": True,
        }
        return {**defaults, **response}
