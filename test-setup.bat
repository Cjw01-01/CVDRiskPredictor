@echo off
echo ========================================
echo Testing Setup - Step by Step
echo ========================================
echo.

echo Step 1: Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo Python found!
echo.

echo Step 2: Checking if we're in the right directory...
if not exist "backend\main.py" (
    echo ERROR: Cannot find backend\main.py
    echo Please run this script from the project root directory
    pause
    exit /b 1
)
echo Directory is correct!
echo.

echo Step 3: Checking model files...
set missing=0
if not exist "backend\hypertension.pt" (
    echo WARNING: hypertension.pt not found
    set missing=1
)
if not exist "backend\cimt_reg.pth" (
    echo WARNING: cimt_reg.pth not found
    set missing=1
)
if not exist "backend\vessel.pth" (
    echo WARNING: vessel.pth not found
    set missing=1
)
if not exist "backend\fusion_cvd_noskewed.pth" (
    echo WARNING: fusion_cvd_noskewed.pth not found
    set missing=1
)
if %missing%==0 (
    echo All model files found!
) else (
    echo WARNING: Some model files are missing
)
echo.

echo Step 4: Checking virtual environment...
cd backend
if not exist "venv" (
    echo Virtual environment does not exist yet
    echo It will be created when you run start-backend.bat
) else (
    echo Virtual environment exists!
)
echo.

echo Step 5: Summary
echo ========================================
echo Setup check complete!
echo.
echo Next steps:
echo 1. Run start-backend.bat to start the backend
echo 2. If you see errors, check STEP_BY_STEP_SETUP.md
echo.
pause

