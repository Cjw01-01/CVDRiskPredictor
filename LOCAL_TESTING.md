# Local Testing Guide

## Quick Start

### Option 1: Use the Batch Files (Windows - Easiest)

1. **Start Backend:**
   - Double-click `start-backend.bat`
   - Wait for "Application startup complete"
   - Backend will be at http://localhost:8000

2. **Start Frontend (in a new terminal):**
   - Double-click `start-frontend.bat`
   - Browser will open automatically at http://localhost:3000

### Option 2: Manual Setup

## Step 1: Setup Backend

1. **Open terminal in project root**

2. **Navigate to backend:**
   ```bash
   cd backend
   ```

3. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

4. **Activate virtual environment:**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Mac/Linux:**
     ```bash
     source venv/bin/activate
     ```

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Make sure model files are in backend directory:**
   - `hypertension.pt`
   - `cimt_reg.pth`
   - `vessel.pth`
   - `fusion_cvd_noskewed.pth`

7. **Run backend:**
   ```bash
   python main.py
   ```

   You should see:
   ```
   INFO:     Started server process
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

8. **Test backend:**
   - Open http://localhost:8000/docs in browser
   - You should see FastAPI documentation
   - Try the `/health` endpoint

## Step 2: Setup Frontend

1. **Open a NEW terminal** (keep backend running)

2. **Navigate to frontend:**
   ```bash
   cd frontend
   ```

3. **Install dependencies:**
   ```bash
   npm install
   ```

4. **Create .env file:**
   Create a file named `.env` in the `frontend` directory with:
   ```
   REACT_APP_API_URL=http://localhost:8000
   ```

5. **Run frontend:**
   ```bash
   npm start
   ```

   Browser should open automatically at http://localhost:3000

## Step 3: Test the Application

1. **Open the app:** http://localhost:3000

2. **Select a model:**
   - Click on one of the 4 model cards

3. **Upload an image:**
   - Click "Click to upload or drag and drop"
   - Select a retinal image (PNG, JPG, JPEG)

4. **Click "Predict CVD Risk"**

5. **View results:**
   - Hypertension: Shows 0 or 1
   - CIMT: Shows numeric value
   - Vessel: Shows masked image
   - Fusion: Shows combined prediction

## Troubleshooting

### Backend Issues

**"Module not found" errors:**
```bash
cd backend
pip install -r requirements.txt
```

**"Model file not found" errors:**
- Make sure all `.pt` and `.pth` files are in the `backend` directory
- Check file names match exactly:
  - `hypertension.pt`
  - `cimt_reg.pth`
  - `vessel.pth`
  - `fusion_cvd_noskewed.pth`

**"Port 8000 already in use":**
- Close other applications using port 8000
- Or change port in `backend/main.py`:
  ```python
  uvicorn.run(app, host="0.0.0.0", port=8001)
  ```

**Model loading errors:**
- Your models might need specific architectures defined
- Check the error message for details
- You may need to modify `backend/main.py` to define model architecture

### Frontend Issues

**"npm: command not found":**
- Install Node.js from https://nodejs.org
- Restart terminal after installation

**"Cannot connect to API":**
- Make sure backend is running on http://localhost:8000
- Check `.env` file has correct URL
- Check browser console for errors (F12)

**"Module not found" errors:**
```bash
cd frontend
rm -rf node_modules
npm install
```

**Port 3000 already in use:**
- React will ask to use a different port
- Or kill the process using port 3000

### General Issues

**CORS errors:**
- Backend should allow `http://localhost:3000`
- Check `backend/main.py` has:
  ```python
  allow_origins=["*"]  # For local testing
  ```

**Image upload not working:**
- Make sure image is valid (PNG, JPG, JPEG)
- Check file size (should be reasonable)
- Check browser console for errors

## Testing Different Models

### Hypertension Model
- Input: Retinal image
- Output: 0 (negative) or 1 (positive)
- Shows confidence percentage

### CIMT Model
- Input: Retinal image
- Output: Numeric value (0.4 - 1.2)
- Represents Carotid Intima-Media Thickness

### Vessel Segmentation
- Input: Retinal image
- Output: Masked image showing vessels
- Black background with highlighted vessels

### Fusion Model
- Input: Retinal image
- Output: Combined prediction
- May show components from other models

## Next Steps

Once local testing works:
1. Test with different images
2. Verify all 4 models work correctly
3. Check prediction accuracy
4. If models need architecture definitions, update `backend/main.py`
5. When ready, deploy following `DEPLOYMENT.md`

## Need Help?

If you encounter model loading errors, you may need to:
1. Check how your models were saved
2. Define the model architecture in `backend/main.py`
3. Adjust preprocessing if models expect different input sizes

Share any error messages and I can help fix them!

