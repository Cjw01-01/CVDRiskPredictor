# Quick Start - Local Testing

## ✅ Step 1: Model Files (Already Done!)
All model files have been copied to the `backend` directory.

## 🐍 Step 2: Setup Backend

**Option A: Use the batch file (Easiest)**
1. Double-click `start-backend.bat`
2. Wait for it to install dependencies and start

**Option B: Manual setup**
Open PowerShell or Command Prompt and run:

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Test backend:**
- Open http://localhost:8000/docs in your browser
- You should see the API documentation

## ⚛️ Step 3: Setup Frontend

**Open a NEW terminal window** (keep backend running!)

**Option A: Use the batch file**
1. Double-click `start-frontend.bat`

**Option B: Manual setup**
```powershell
cd frontend
npm install
npm start
```

The browser should open automatically at http://localhost:3000

## 🎯 Step 4: Test the App

1. **Select a model** - Click on one of the 4 model cards
2. **Upload an image** - Click "Click to upload" and select a retinal image
3. **Click "Predict CVD Risk"**
4. **View results!**

## ⚠️ Important Notes

### If you get model loading errors:
Your models might need specific architectures. The current code tries to load them generically, but if they were saved with a specific architecture, you may need to:

1. Check the error message
2. Define the model architecture in `backend/main.py`
3. Load the state dict instead of the full model

### Frontend .env file:
Create a file named `.env` in the `frontend` directory with:
```
REACT_APP_API_URL=http://localhost:8000
```

## 🐛 Troubleshooting

**Backend won't start:**
- Make sure Python 3.8+ is installed
- Check that all model files are in `backend/` directory
- Try: `pip install --upgrade pip` then `pip install -r requirements.txt`

**Frontend won't start:**
- Make sure Node.js is installed (https://nodejs.org)
- Try: `npm install` again
- Check that `.env` file exists in `frontend/` directory

**CORS errors:**
- Backend should allow `http://localhost:3000`
- Check `backend/main.py` line with `allow_origins=["*"]`

**Port already in use:**
- Close other applications using ports 8000 or 3000
- Or change ports in the code

## 📝 Next Steps

Once everything works locally:
1. Test all 4 models
2. Verify predictions look correct
3. When ready, follow `DEPLOYMENT.md` to deploy

Need help? Check the error messages and let me know!

