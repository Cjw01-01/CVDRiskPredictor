@echo off
REM Fix Virtual Environment Script
echo ========================================
echo Fixing Virtual Environment
echo ========================================
echo.

cd /d "%~dp0backend"
if errorlevel 1 (
    echo ERROR: Cannot find backend directory!
    pause
    exit /b 1
)

echo Step 1: Removing old/incomplete virtual environment...
if exist "venv" (
    rmdir /s /q venv
    echo Old venv removed.
) else (
    echo No old venv found.
)
echo.

echo Step 2: Creating new virtual environment...
python -m venv venv
if errorlevel 1 (
    echo.
    echo ERROR: Failed to create virtual environment!
    echo Make sure Python is installed correctly.
    pause
    exit /b 1
)
echo Virtual environment created!
echo.

echo Step 3: Verifying activation script exists...
if exist "venv\Scripts\activate.bat" (
    echo SUCCESS: activate.bat found!
) else (
    echo ERROR: activate.bat still not found!
    echo The virtual environment may be corrupted.
    pause
    exit /b 1
)
echo.

echo Step 4: Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate!
    pause
    exit /b 1
)
echo Activated! (You should see (venv) in prompt)
echo.

echo Step 5: Upgrading pip...
python -m pip install --upgrade pip
echo.

echo Step 6: Installing dependencies...
echo This will take 2-5 minutes, please wait...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo WARNING: Some packages may have failed to install.
    echo.
)
echo.

echo ========================================
echo Virtual environment is ready!
echo ========================================
echo.
echo Now you can start the server with:
echo   python main.py
echo.
echo Or use SIMPLE_START.bat from the project root.
echo.
pause

