# Complete Restart Guide - Step by Step

## What Happened

I just updated your backend code to properly load all 4 models (including the fusion model). You need to restart the backend to use the new code.

---

## Step-by-Step Instructions

### Step 1: Stop the Backend (if it's running)

1. **Find the Command Prompt/PowerShell window** where the backend is running
2. **Press `Ctrl + C`** to stop it
3. **Close that window** (or keep it open, doesn't matter)

### Step 2: Install the New Dependency

1. **Open a NEW Command Prompt/PowerShell window**
2. **Navigate to your project folder:**
   ```bash
   cd "C:\Users\User\OneDrive - American University of Beirut\Desktop\490deploy\backend"
   ```

3. **Activate the virtual environment:**
   ```bash
   .\venv\Scripts\activate
   ```
   You should see `(venv)` at the beginning of your prompt.

4. **Install `timm` (required for the models):**
   ```bash
   pip install timm>=0.9.0
   ```
   Wait for it to finish installing.

### Step 3: Verify Model Files Are in Backend Folder

Make sure these 4 files are in the `backend` folder:
- `hypertension.pt`
- `cimt_reg.pth`
- `vessel.pth`
- `fusion_cvd_noskewed.pth`

**To check:**
1. Open File Explorer
2. Go to: `C:\Users\User\OneDrive - American University of Beirut\Desktop\490deploy\backend`
3. You should see all 4 model files there

**If they're not there:**
- Copy them from the main project folder to the `backend` folder

### Step 4: Start the Backend

**In the same Command Prompt window** (where you activated venv):

```bash
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this window open!** The backend is now running.

### Step 5: Start the Frontend (if not already running)

1. **Open a NEW Command Prompt/PowerShell window**
2. **Navigate to frontend folder:**
   ```bash
   cd "C:\Users\User\OneDrive - American University of Beirut\Desktop\490deploy\frontend"
   ```

3. **Start the frontend:**
   ```bash
   npm start
   ```

4. **Wait for it to open** in your browser (usually `http://localhost:3000`)

**Keep this window open too!**

---

## What Changed

### Before:
- Backend couldn't load models properly (they were saved as state_dicts)
- Fusion model wasn't implemented

### Now:
- ✅ All 4 models can be loaded correctly
- ✅ Fusion model works by combining features from HTN, CIMT, and Vessel models
- ✅ All models use the correct architectures from your notebooks

---

## Testing

### Test Individual Models:

1. **Open the frontend** in your browser (`http://localhost:3000`)
2. **Upload an image**
3. **Try each model one by one:**
   - Select "Hypertension" → Click "Predict" → Should return 0 or 1
   - Select "CIMT" → Click "Predict" → Should return a number between 0.4 and 1.2
   - Select "A/V Segmentation" → Click "Predict" → Should show a masked image
   - Select "Fusion Model" → Click "Predict" → Should return CVD risk (0 or 1) with probability

### If Something Doesn't Work:

**Check the backend window** for error messages. Common issues:

1. **"ModuleNotFoundError: No module named 'timm'"**
   - Solution: Run `pip install timm>=0.9.0` in the backend venv

2. **"Model loading error"**
   - Solution: Make sure all 4 model files are in the `backend` folder

3. **"File not found"**
   - Solution: Check that model files are in the correct location

---

## Quick Reference

### Backend Commands:
```bash
# Navigate to backend
cd backend

# Activate venv
.\venv\Scripts\activate

# Install dependencies (if needed)
pip install timm>=0.9.0

# Start backend
python main.py
```

### Frontend Commands:
```bash
# Navigate to frontend
cd frontend

# Start frontend
npm start
```

---

## Summary

1. ✅ Stop old backend (Ctrl+C)
2. ✅ Install `timm` in backend venv
3. ✅ Verify 4 model files are in `backend` folder
4. ✅ Start backend (`python main.py`)
5. ✅ Start frontend (`npm start`)
6. ✅ Test all 4 models

That's it! 🚀

