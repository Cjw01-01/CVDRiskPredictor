# Fix "Failed to fetch" Error

## The Problem
Your frontend is running but can't connect to the backend. This happens when:
1. Backend is not running
2. .env file is missing or wrong

## Solution

### Step 1: Make Sure Backend is Running

1. **Check if you still have the backend window open**
   - Look for a Command Prompt window showing:
     ```
     INFO: Uvicorn running on http://0.0.0.0:8000
     ```
   - If you closed it, the backend stopped!

2. **If backend is NOT running:**
   - Go back to the project folder
   - Double-click `SIMPLE_START.bat` (or use the method that worked before)
   - Wait for: `INFO: Uvicorn running on http://0.0.0.0:8000`
   - **Keep that window open!**

### Step 2: Create .env File (If Missing)

The `.env` file should be in the `frontend` folder.

**Quick method:**
1. Go to project root folder
2. Double-click `create-env.bat`

**Or manually:**
1. Open `frontend` folder in File Explorer
2. Create `.env` file with content:
   ```
   REACT_APP_API_URL=http://localhost:8000
   ```

### Step 3: Restart Frontend

After creating/updating `.env`:

1. **Stop the frontend** (in the terminal where `npm start` is running):
   - Press `Ctrl + C`

2. **Restart it:**
   ```cmd
   npm start
   ```

3. **Wait for browser to refresh**

### Step 4: Test Connection

1. **Open browser** to http://localhost:3000
2. **Select a model** (e.g., Hypertension)
3. **Upload an image**
4. **Click "Predict CVD Risk"**

If it still says "Failed to fetch":
- Check that backend window is still open and running
- Check browser console (F12) for errors
- Verify `.env` file exists in `frontend` folder

## Quick Checklist

- [ ] Backend is running (window shows "Uvicorn running on http://0.0.0.0:8000")
- [ ] `.env` file exists in `frontend` folder
- [ ] `.env` contains: `REACT_APP_API_URL=http://localhost:8000`
- [ ] Frontend was restarted after creating `.env`
- [ ] Both backend and frontend are running at the same time

## Still Not Working?

1. **Test backend directly:**
   - Open http://localhost:8000/docs in browser
   - If this doesn't work, backend is not running

2. **Check browser console:**
   - Press F12 in browser
   - Go to "Console" tab
   - Look for error messages
   - Share the error with me

