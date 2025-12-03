# Step-by-Step Setup Guide

## Step 1: Start the Backend Server

### Method 1: Using the Batch File (Recommended)

1. **Open File Explorer** and navigate to:
   ```
   C:\Users\User\OneDrive - American University of Beirut\Desktop\490deploy
   ```

2. **Double-click** on `start-backend.bat`

3. **A black command window will open** - this is normal!

4. **Watch for these messages:**
   - "Creating virtual environment..." (first time only)
   - "Installing/updating dependencies..."
   - "Backend server starting on http://localhost:8000"
   - "INFO: Uvicorn running on http://0.0.0.0:8000"

5. **If you see errors**, scroll down to the "Troubleshooting" section below.

6. **Keep this window open!** The backend must stay running.

### Method 2: Manual Setup (If batch file doesn't work)

1. **Open PowerShell or Command Prompt:**
   - Press `Windows Key + R`
   - Type `powershell` and press Enter

2. **Navigate to the project folder:**
   ```powershell
   cd "C:\Users\User\OneDrive - American University of Beirut\Desktop\490deploy\backend"
   ```

3. **Create virtual environment (if not exists):**
   ```powershell
   python -m venv venv
   ```
   Wait for it to finish (may take 30 seconds)

4. **Activate the virtual environment:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   
   **If you get an error about execution policy**, run this first:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   Then try activating again.

   **Alternative (if PowerShell doesn't work):**
   ```cmd
   venv\Scripts\activate.bat
   ```

5. **You should see `(venv)` at the start of your prompt** - this means it's activated!

6. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
   This will take 2-5 minutes. Wait for it to finish.

7. **Start the server:**
   ```powershell
   python main.py
   ```

8. **You should see:**
   ```
   INFO:     Started server process
   INFO:     Uvicorn running on http://0.0.0.0:8000
   INFO:     Application startup complete.
   ```

9. **Keep this window open!**

### Verify Backend is Working

1. **Open your web browser** (Chrome, Edge, Firefox)

2. **Go to:** http://localhost:8000/docs

3. **You should see** a page with "FastAPI" and API documentation

4. **If you see this, backend is working! ✅**

## Step 2: Create Frontend Environment File

1. **Open File Explorer** and go to:
   ```
   C:\Users\User\OneDrive - American University of Beirut\Desktop\490deploy\frontend
   ```

2. **Right-click** in the empty space → **New** → **Text Document**

3. **Name it exactly:** `.env` (including the dot at the start)

   **If Windows won't let you name it `.env`:**
   - Name it `env.txt` first
   - Then rename it to `.env` (Windows will warn you - click Yes)

4. **Right-click** `.env` → **Open with** → **Notepad**

5. **Type this exactly:**
   ```
   REACT_APP_API_URL=http://localhost:8000
   ```

6. **Save and close** (Ctrl+S, then close Notepad)

## Step 3: Start the Frontend

1. **Open a NEW PowerShell window** (keep the backend window open!)

   - Press `Windows Key + R`
   - Type `powershell` and press Enter

2. **Navigate to frontend:**
   ```powershell
   cd "C:\Users\User\OneDrive - American University of Beirut\Desktop\490deploy\frontend"
   ```

3. **Install dependencies (first time only):**
   ```powershell
   npm install
   ```
   This takes 2-5 minutes. Wait for it to finish.

4. **Start the frontend:**
   ```powershell
   npm start
   ```

5. **Your browser should automatically open** to http://localhost:3000

6. **You should see** the beautiful CVD Risk Predictor interface!

## Troubleshooting Step 1 (Backend)

### Error: "python is not recognized"
**Solution:** Python is not installed or not in PATH
1. Download Python from https://www.python.org/downloads/
2. During installation, check "Add Python to PATH"
3. Restart your computer
4. Try again

### Error: "pip is not recognized"
**Solution:** Same as above - install Python properly

### Error: "Execution Policy" error in PowerShell
**Solution:** Run this command:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then try activating the virtual environment again.

### Error: "ModuleNotFoundError" or "No module named 'fastapi'"
**Solution:** Dependencies didn't install properly
1. Make sure virtual environment is activated (you see `(venv)`)
2. Run: `pip install --upgrade pip`
3. Run: `pip install -r requirements.txt` again

### Error: "Model file not found"
**Solution:** Model files are missing
1. Check that these files exist in `backend` folder:
   - `hypertension.pt`
   - `cimt_reg.pth`
   - `vessel.pth`
   - `fusion_cvd_noskewed.pth`
2. If missing, copy them from the main folder

### Error: "Port 8000 already in use"
**Solution:** Something else is using port 8000
1. Close other applications
2. Or change the port in `backend/main.py` (last line):
   ```python
   uvicorn.run(app, host="0.0.0.0", port=8001)
   ```
   Then use `http://localhost:8001` instead

### Error: Model loading errors
**Solution:** This is expected if models need specific architectures
1. Note the exact error message
2. The models might need architecture definitions
3. We can fix this once we see the error

### Backend starts but shows errors
**Don't worry!** As long as you see:
```
INFO: Uvicorn running on http://0.0.0.0:8000
```
The server is running. Model errors will only appear when you try to predict.

## What Should You See?

### When Backend Starts Successfully:
```
(venv) PS C:\Users\User\...\backend> python main.py
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### When Frontend Starts Successfully:
```
Compiled successfully!

You can now view cvd-risk-predictor-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

## Still Stuck?

**Tell me:**
1. What error message do you see? (Copy the exact text)
2. At which step are you stuck?
3. What happens when you run `start-backend.bat`?

I'll help you fix it!

