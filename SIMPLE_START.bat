@echo off
REM Simple Backend Starter - Works in Command Prompt
echo.
echo ========================================
echo CVD Risk Predictor - Backend Server
echo ========================================
echo.

REM Change to backend directory
cd /d "%~dp0backend"
if errorlevel 1 (
    echo ERROR: Cannot find backend directory!
    echo Make sure this file is in the project root.
    pause
    exit /b 1
)

REM Check if venv exists, create if not
if not exist "venv" (
    echo Step 1: Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo.
        echo ERROR: Python not found or virtual environment creation failed!
        echo Please make sure Python is installed.
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
    echo.
)

REM Activate virtual environment
echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo.
    echo ERROR: Cannot activate virtual environment!
    echo The venv\Scripts\activate.bat file may be missing.
    pause
    exit /b 1
)
echo Activated! (You should see (venv) in the prompt)
echo.

REM Install dependencies
echo Step 3: Installing dependencies...
echo This may take a few minutes, please wait...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo WARNING: Some packages may have failed to install.
    echo The server might still work, but errors may occur.
    echo.
)

echo.
echo Step 4: Starting server...
echo.
echo ========================================
echo Server will start on http://localhost:8000
echo Open http://localhost:8000/docs in your browser to test
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start the server
python main.py

REM If we get here, the server stopped
echo.
echo Server stopped.
pause

