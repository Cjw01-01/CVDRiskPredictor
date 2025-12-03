@echo off
echo ============================================================
echo REMOVING HUGGING FACE TOKEN FROM GIT HISTORY
echo ============================================================
echo.
echo This script will:
echo 1. Create a backup branch
echo 2. Remove the token from git history
echo 3. Prepare for force push
echo.
pause

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo Using Python script...
    python fix_token_history.py
) else (
    echo Python not found. Using PowerShell method...
    powershell -ExecutionPolicy Bypass -File fix-git-history-simple.ps1
)

echo.
echo ============================================================
echo DONE! Now run: git push origin main --force
echo ============================================================
pause


