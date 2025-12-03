@echo off
echo ========================================
echo Pushing CVD Risk Predictor to GitHub
echo Repository: https://github.com/Cjw01-01/CVDRiskPredictor.git
echo ========================================
echo.

REM Check if git is available
where git >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Git is not installed or not in PATH
    echo.
    echo Please install Git from: https://git-scm.com/download/win
    echo Or use GitHub Desktop: https://desktop.github.com/
    echo.
    pause
    exit /b 1
)

echo [1/5] Initializing git repository...
git init
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to initialize git
    pause
    exit /b 1
)

echo [2/5] Adding remote repository...
git remote remove origin 2>nul
git remote add origin https://github.com/Cjw01-01/CVDRiskPredictor.git
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to add remote
    pause
    exit /b 1
)

echo [3/5] Adding all files...
git add .
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to add files
    pause
    exit /b 1
)

echo [4/5] Committing changes...
git commit -m "Initial commit: CVD Risk Predictor with Netlify Functions setup"
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to commit
    pause
    exit /b 1
)

echo [5/5] Pushing to GitHub...
git branch -M main
git push -u origin main
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Failed to push to GitHub
    echo.
    echo Possible reasons:
    echo - Repository doesn't exist or you don't have access
    echo - Need to authenticate (GitHub may prompt for credentials)
    echo - Network connection issue
    echo.
    echo Try running these commands manually:
    echo   git branch -M main
    echo   git push -u origin main
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS! Project pushed to GitHub
echo ========================================
echo.
echo Repository: https://github.com/Cjw01-01/CVDRiskPredictor
echo.
pause



