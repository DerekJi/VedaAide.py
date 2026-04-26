@echo off
REM Start PR Monitor Daemon (Windows)

setlocal enabledelayedexpansion

cd /d "%~dp0"

echo 🚀 Starting PR Monitor Daemon...
echo.

REM Check for .env file
if not exist .env (
    echo ⚠️  .env file not found!
    echo Please copy .env.example to .env and configure it:
    echo   copy .env.example .env
    echo   rem Edit .env with your GitHub token and Claude API key
    exit /b 1
)

REM Load environment variables from .env
for /f "delims=" %%i in ('findstr /R "^[^#]" .env') do set %%i

REM Check for required variables
if "!GITHUB_TOKEN!"=="" (
    echo ❌ GITHUB_TOKEN not set in .env
    exit /b 1
)

if "!CLAUDE_API_KEY!"=="" (
    echo ❌ CLAUDE_API_KEY not set in .env
    exit /b 1
)

echo ✓ Configuration loaded
echo ✓ GitHub: !GITHUB_OWNER!/!GITHUB_REPO!
echo ✓ Monitor interval: !PR_MONITOR_INTERVAL! seconds
echo ✓ Trusted users: !TRUSTED_USERS!
echo.

REM Create state directory if not exists
if not exist state mkdir state

REM Start monitor
echo 📡 Monitoring PR comments...
echo Log file: !cd!\state\monitor.log
echo.
echo Press Ctrl+C to stop
echo.

python pr_monitor.py

endlocal
