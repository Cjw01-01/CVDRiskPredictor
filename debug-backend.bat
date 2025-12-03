@echo off
echo ========================================
echo Backend Debug Script
echo ========================================
echo.

echo Current directory:
cd
echo.

echo Checking Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)
echo.

echo Changing to backend directory...
cd backend
if %errorlevel% neq 0 (
    echo ERROR: Cannot find backend directory!
    pause
    exit /b 1
)
echo Current directory: %CD%
echo.

echo Checking for model files...
dir *.pt *.pth /b
echo.

echo Checking virtual environment...
if exist "venv" (
    echo Virtual environment exists
    if exist "venv\Scripts\python.exe" (
        echo Virtual environment Python found
        venv\Scripts\python.exe --version
    ) else (
        echo WARNING: Virtual environment Python not found
    )
) else (
    echo Virtual environment does not exist - will create it
)
echo.

echo Attempting to activate virtual environment...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    if errorlevel 1 (
        echo ERROR: Failed to activate virtual environment!
        pause
        exit /b 1
    )
    echo Virtual environment activated!
    echo.
    echo Checking pip...
    pip --version
    echo.
    echo Checking installed packages...
    pip list | findstr "fastapi uvicorn torch"
    echo.
    echo ========================================
    echo If you see fastapi, uvicorn, and torch above, dependencies are installed
    echo ========================================
    echo.
    echo Attempting to start server...
    echo (Press Ctrl+C to stop)
    echo.
    python main.py
) else (
    echo Virtual environment not set up yet.
    echo.
    echo Creating virtual environment...
    python -m venv venv
    echo.
    echo Activating...
    call venv\Scripts\activate.bat
    echo.
    echo Installing dependencies (this will take a few minutes)...
    pip install --upgrade pip
    pip install -r requirements.txt
    echo.
    echo Dependencies installed! Starting server...
    echo (Press Ctrl+C to stop)
    echo.
    python main.py
)

pause

