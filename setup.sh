#!/bin/bash

# Setup script for CVD Risk Predictor

echo "🚀 Setting up CVD Risk Predictor..."

# Copy model files to backend
echo "📦 Copying model files to backend..."
cp hypertension.pt backend/ 2>/dev/null || echo "⚠️  hypertension.pt not found"
cp cimt_reg.pth backend/ 2>/dev/null || echo "⚠️  cimt_reg.pth not found"
cp vessel.pth backend/ 2>/dev/null || echo "⚠️  vessel.pth not found"
cp fusion_cvd_noskewed.pth backend/ 2>/dev/null || echo "⚠️  fusion_cvd_noskewed.pth not found"

echo "✅ Model files copied!"

# Setup backend
echo "🐍 Setting up backend..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

source venv/bin/activate
pip install -r requirements.txt
echo "✅ Backend dependencies installed"
cd ..

# Setup frontend
echo "⚛️  Setting up frontend..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
    echo "✅ Frontend dependencies installed"
else
    echo "✅ Frontend dependencies already installed"
fi
cd ..

echo ""
echo "✨ Setup complete!"
echo ""
echo "To run backend:"
echo "  cd backend && source venv/bin/activate && python main.py"
echo ""
echo "To run frontend:"
echo "  cd frontend && npm start"
echo ""

