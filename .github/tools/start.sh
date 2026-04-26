#!/bin/bash
# Start PR Monitor Daemon

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 Starting PR Monitor Daemon..."
echo ""

# Check for .env file
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "Please copy .env.example to .env and configure it:"
    echo "  cp .env.example .env"
    echo "  # Edit .env with your GitHub token and Claude API key"
    exit 1
fi

# Load environment variables
set -a
source .env
set +a

# Check for required variables
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ GITHUB_TOKEN not set in .env"
    exit 1
fi

if [ -z "$CLAUDE_API_KEY" ]; then
    echo "❌ CLAUDE_API_KEY not set in .env"
    exit 1
fi

echo "✓ Configuration loaded"
echo "✓ GitHub: $GITHUB_OWNER/$GITHUB_REPO"
echo "✓ Monitor interval: $PR_MONITOR_INTERVAL seconds"
echo "✓ Trusted users: $TRUSTED_USERS"
echo ""

# Create state directory if not exists
mkdir -p state

# Start monitor
echo "📡 Monitoring PR comments..."
echo "Log file: $(pwd)/state/monitor.log"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python pr_monitor.py
