@echo off
REM Setup script for CVD Risk Predictor (Windows)

echo 🚀 Setting up CVD Risk Predictor...

REM Copy model files to backend
echo 📦 Copying model files to backend...
copy hypertension.pt backend\ 2>nul || echo ⚠️  hypertension.pt not found
copy cimt_reg.pth backend\ 2>nul || echo ⚠️  cimt_reg.pth not found
copy vessel.pth backend\ 2>nul || echo ⚠️  vessel.pth not found
copy fusion_cvd_noskewed.pth backend\ 2>nul || echo ⚠️  fusion_cvd_noskewed.pth not found

echo ✅ Model files copied!

REM Setup backend
echo 🐍 Setting up backend...
cd backend
if not exist "venv" (
    python -m venv venv
    echo ✅ Virtual environment created
)

call venv\Scripts\activate.bat
pip install -r requirements.txt
echo ✅ Backend dependencies installed
cd ..

REM Setup frontend
echo ⚛️  Setting up frontend...
cd frontend
if not exist "node_modules" (
    call npm install
    echo ✅ Frontend dependencies installed
) else (
    echo ✅ Frontend dependencies already installed
)
cd ..

echo.
echo ✨ Setup complete!
echo.
echo To run backend:
echo   cd backend ^&^& venv\Scripts\activate ^&^& python main.py
echo.
echo To run frontend:
echo   cd frontend ^&^& npm start
echo.

pause

