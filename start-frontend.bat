@echo off
echo Starting Frontend Development Server...
cd frontend
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
)
echo.
echo ========================================
echo Frontend starting on http://localhost:3000
echo Make sure backend is running on http://localhost:8000
echo ========================================
echo.
call npm start

