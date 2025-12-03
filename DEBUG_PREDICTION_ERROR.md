# Debug Prediction Error

## What's Happening
The frontend is working, but when you click "Predict CVD Risk", you get a "Prediction error". This usually means:
1. Backend received the request
2. But something went wrong when loading/running the model

## Step 1: Check Backend Window

Look at your **backend Command Prompt window** (the one showing "Uvicorn running").

**What error message do you see there?**

Common errors:
- `Error loading model: ...`
- `Model architecture not defined`
- `FileNotFoundError: ...`
- `RuntimeError: ...`

## Step 2: Check Browser Console

1. **Press F12** in your browser (on the localhost:3000 page)
2. Click the **"Console"** tab
3. **Look for red error messages**
4. **Copy the error text** and share it

## Common Issues & Fixes

### Issue: Model Loading Error
**Error might say:** "Error loading model" or "Unknown model architecture"

**Why:** Your models were saved with specific architectures, but the code doesn't know what they are.

**Fix:** We need to define the model architecture. Share the error message and I'll help you fix it.

### Issue: Model File Not Found
**Error might say:** "FileNotFoundError" or "No such file or directory"

**Fix:** Make sure all model files are in the `backend` folder:
- `hypertension.pt`
- `cimt_reg.pth`
- `vessel.pth`
- `fusion_cvd_noskewed.pth`

### Issue: Image Processing Error
**Error might say:** Something about image size or format

**Fix:** The image might need different preprocessing. Share the error.

## What to Do Now

1. **Check the backend window** - what error appears there?
2. **Check browser console (F12)** - what errors are there?
3. **Share both error messages** with me

Then I can help you fix the specific issue!

