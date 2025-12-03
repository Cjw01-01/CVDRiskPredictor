@echo off
echo ========================================
echo Starting Backend Server...
echo ========================================
echo.

cd /d "%~dp0backend"
if errorlevel 1 (
    echo ERROR: Cannot find backend directory!
    pause
    exit /b 1
)

echo Current directory: %CD%
echo.

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment!
        echo Make sure Python is installed and in PATH.
        pause
        exit /b 1
    )
    echo Virtual environment created!
    echo.
)

echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)

echo Virtual environment activated!
echo.

echo Installing/updating dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo WARNING: Some dependencies may have failed to install
    echo Continuing anyway...
    echo.
)

echo.
echo ========================================
echo Backend server starting on http://localhost:8000
echo API docs available at http://localhost:8000/docs
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py
if errorlevel 1 (
    echo.
    echo ERROR: Server failed to start!
    echo Check the error messages above.
    pause
)

