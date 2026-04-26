"""PR Monitor Configuration."""

import os
from pathlib import Path

# GitHub Configuration
GITHUB_OWNER = os.getenv("GITHUB_OWNER", "DerekJi")
GITHUB_REPO = os.getenv("GITHUB_REPO", "VedaAide.py")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

# Monitor Configuration
POLL_INTERVAL_SECONDS = int(os.getenv("PR_MONITOR_INTERVAL", "1800"))  # 30 minutes default
STATE_DIR = Path(__file__).parent / "state"
PROCESSED_COMMENTS_FILE = STATE_DIR / "processed_comments.json"
MONITOR_LOG_FILE = STATE_DIR / "monitor.log"

# Execution Configuration
AUTO_COMMIT = os.getenv("AUTO_COMMIT", "true").lower() == "true"
AUTO_PUSH = os.getenv("AUTO_PUSH", "true").lower() == "true"
VERIFY_BEFORE_COMMIT = os.getenv("VERIFY_BEFORE_COMMIT", "true").lower() == "true"

# Copilot Chat Configuration (VS Code Extension)
# The PR Monitor daemon will communicate with a Copilot Chat API
# exposed by the VS Code extension at this endpoint
COPILOT_CHAT_HOST = os.getenv("COPILOT_CHAT_HOST", "localhost")
COPILOT_CHAT_PORT = int(os.getenv("COPILOT_CHAT_PORT", "3456"))
COPILOT_CHAT_URL = f"http://{COPILOT_CHAT_HOST}:{COPILOT_CHAT_PORT}"

# Safety Configuration
# Only process comments from these GitHub users
TRUSTED_USERS = set(os.getenv("TRUSTED_USERS", "DerekJi,derekj_youi").split(","))

# Don't modify files matching these patterns
PROTECTED_PATHS = [
    ".git/**",
    ".github/**",
    "node_modules/**",
    "*.lock",
    "*.egg-info/**",
    ".venv/**",
    "venv/**",
]

# Categories of changes to allow
ALLOWED_CHANGE_TYPES = {
    "docs",  # Documentation updates
    "config",  # Configuration files
    "test",  # Test files
    "code",  # Source code
    "data",  # Data files
}

# Repository root
REPO_ROOT = Path(__file__).parent.parent.parent
