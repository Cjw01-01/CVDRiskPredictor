#!/bin/bash

echo "========================================"
echo "Pushing CVD Risk Predictor to GitHub"
echo "Repository: https://github.com/Cjw01-01/CVDRiskPredictor.git"
echo "========================================"
echo ""

# Navigate to project directory
cd /c/cvddeploy

# Initialize git repository
echo "[1/5] Initializing git repository..."
git init

# Add remote repository
echo "[2/5] Adding remote repository..."
git remote remove origin 2>/dev/null
git remote add origin https://github.com/Cjw01-01/CVDRiskPredictor.git

# Add all files
echo "[3/5] Adding all files..."
git add .

# Commit
echo "[4/5] Committing changes..."
git commit -m "Initial commit: CVD Risk Predictor with Netlify Functions setup"

# Push to GitHub
echo "[5/5] Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "========================================"
echo "SUCCESS! Project pushed to GitHub"
echo "========================================"
echo ""
echo "Repository: https://github.com/Cjw01-01/CVDRiskPredictor"
echo ""



