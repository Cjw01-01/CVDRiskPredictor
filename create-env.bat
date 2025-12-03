@echo off
REM Create .env file for frontend
echo ========================================
echo Creating .env file for frontend
echo ========================================
echo.

cd /d "%~dp0frontend"
if errorlevel 1 (
    echo ERROR: Cannot find frontend directory!
    pause
    exit /b 1
)

echo Current directory: %CD%
echo.

if exist ".env" (
    echo .env file already exists!
    echo.
    echo Current content:
    type .env
    echo.
    set /p overwrite="Do you want to overwrite it? (Y/N): "
    if /i not "%overwrite%"=="Y" (
        echo Keeping existing .env file.
        pause
        exit /b 0
    )
)

echo Creating .env file...
echo REACT_APP_API_URL=http://localhost:8000 > .env
if errorlevel 1 (
    echo ERROR: Failed to create .env file!
    pause
    exit /b 1
)

echo.
echo SUCCESS! .env file created!
echo.
echo File location: %CD%\.env
echo.
echo File content:
type .env
echo.
echo ========================================
echo .env file is ready!
echo You can now start the frontend with: npm start
echo ========================================
echo.
pause

