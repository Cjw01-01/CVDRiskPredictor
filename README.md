---
title: CVD Risk Predictor
emoji: 🫀
colorFrom: red
colorTo: blue
sdk: docker
sdk_version: "4.0.0"
app_file: app.py
pinned: false
---

# CVD Risk Predictor

AI-Powered Cardiovascular Disease Risk Assessment from Retinal Images

## Features

- **4 Model Options:**
  - Hypertension Detection (Binary Classification)
  - CIMT Regression (Carotid Intima-Media Thickness)
  - A/V Segmentation (Vessel Masking)
  - Fusion Model (Combined CVD Risk Prediction)

- **Beautiful Modern UI** with gradient design
- **Real-time Predictions** with loading states
- **Image Preview** before prediction
- **Responsive Design** for all devices

## How to Use

1. Select a model from the options
2. Upload a retinal image (or two images for CIMT/Fusion models)
3. Click predict and view results

## Models

Models are automatically loaded from: `carlwakim/cvd-risk-models`
