# Visual Step-by-Step Guide

## 🎯 Your Current Status

✅ Python 3.11.9 is installed  
✅ All model files are in the backend folder  
✅ Virtual environment exists  
✅ All code files are ready  

## 📋 Step 1: Start Backend - DETAILED

### Option A: Using the Batch File (Easiest)

1. **Go to your project folder** in File Explorer:
   ```
   C:\Users\User\OneDrive - American University of Beirut\Desktop\490deploy
   ```

2. **Find the file:** `start-backend.bat`

3. **Double-click it**

4. **A black window will appear** - this is your backend server!

5. **What you should see:**

   ```
   Starting Backend Server...
   Creating virtual environment... (only first time)
   Installing/updating dependencies...
   Collecting fastapi...
   Collecting uvicorn...
   ... (lots of text)
   Successfully installed fastapi-0.104.1 uvicorn-0.24.0 ...
   
   ========================================
   Backend server starting on http://localhost:8000
   API docs available at http://localhost:8000/docs
   ========================================
   
   INFO:     Started server process [12345]
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
   ```

6. **If you see the last line** (`Uvicorn running...`), **SUCCESS! ✅**

7. **DO NOT CLOSE THIS WINDOW** - keep it open!

### Option B: Manual PowerShell Method

1. **Open PowerShell:**
   - Press `Windows Key`
   - Type `PowerShell`
   - Press Enter

2. **Copy and paste this command** (one line at a time):

   ```powershell
   cd "C:\Users\User\OneDrive - American University of Beirut\Desktop\490deploy\backend"
   ```

   Press Enter

3. **Activate virtual environment:**

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   **If you get an error**, run this first:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   Then try activating again.

   **You should see `(venv)` at the start of your line** like this:
   ```
   (venv) PS C:\Users\User\...\backend>
   ```

4. **Install dependencies** (if not already installed):

   ```powershell
   pip install -r requirements.txt
   ```

   Wait for it to finish (2-5 minutes). You'll see:
   ```
   Successfully installed fastapi-0.104.1 ...
   ```

5. **Start the server:**

   ```powershell
   python main.py
   ```

6. **You should see:**

   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

7. **Keep this window open!**

## ✅ Step 2: Verify Backend is Working

1. **Open your web browser** (Chrome, Edge, or Firefox)

2. **Type in the address bar:**
   ```
   http://localhost:8000/docs
   ```

3. **Press Enter**

4. **You should see:**
   - A page with "FastAPI" at the top
   - API documentation with endpoints listed
   - A section showing `/predict` endpoint

   **If you see this, your backend is working! ✅**

## 📝 Step 3: Create Frontend .env File

1. **Open File Explorer**

2. **Navigate to:**
   ```
   C:\Users\User\OneDrive - American University of Beirut\Desktop\490deploy\frontend
   ```

3. **Right-click** in the empty space → **New** → **Text Document**

4. **Rename it to:** `.env`
   - Delete "New Text Document.txt"
   - Type: `.env`
   - Windows will warn you - click **Yes**

5. **Right-click** `.env` → **Open with** → **Notepad**

6. **Type this exactly** (no spaces, no quotes):
   ```
   REACT_APP_API_URL=http://localhost:8000
   ```

7. **Save:** Press `Ctrl + S`

8. **Close Notepad**

## 🚀 Step 4: Start Frontend

1. **Open a NEW PowerShell window** (keep backend running!)

2. **Copy and paste:**

   ```powershell
   cd "C:\Users\User\OneDrive - American University of Beirut\Desktop\490deploy\frontend"
   ```

3. **Install dependencies** (first time only):

   ```powershell
   npm install
   ```

   Wait 2-5 minutes. You'll see:
   ```
   added 1234 packages
   ```

4. **Start frontend:**

   ```powershell
   npm start
   ```

5. **Your browser should automatically open** to:
   ```
   http://localhost:3000
   ```

6. **You should see** the beautiful CVD Risk Predictor interface!

## 🎉 Success Checklist

- [ ] Backend window shows "Uvicorn running on http://0.0.0.0:8000"
- [ ] http://localhost:8000/docs opens and shows API documentation
- [ ] Frontend .env file created with correct content
- [ ] Frontend starts and browser opens to http://localhost:3000
- [ ] You can see the model selection interface

## 🆘 Common Issues & Solutions

### Issue: "python is not recognized"
**Fix:** 
1. Install Python from https://www.python.org/downloads/
2. During installation, check ✅ "Add Python to PATH"
3. Restart computer
4. Try again

### Issue: PowerShell execution policy error
**Fix:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Type `Y` and press Enter

### Issue: "pip is not recognized"
**Fix:** Same as Python issue above - reinstall Python with PATH option

### Issue: Backend window closes immediately
**Fix:**
1. Open PowerShell in the backend folder
2. Run commands manually (see Option B above)
3. This will show you the actual error

### Issue: "Module not found" errors
**Fix:**
1. Make sure virtual environment is activated (you see `(venv)`)
2. Run: `pip install -r requirements.txt` again

### Issue: Port 8000 already in use
**Fix:**
1. Close other programs
2. Or change port in `backend/main.py` last line to `port=8001`

## 📞 Need Help?

**Tell me exactly:**
1. What command did you run?
2. What error message appeared? (copy the exact text)
3. At which step number are you stuck?

I'll help you fix it!

