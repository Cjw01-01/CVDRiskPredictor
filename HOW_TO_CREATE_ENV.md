# How to Create .env File - Correct Steps

## Important: You need to be INSIDE the frontend folder!

### Step 1: Open the frontend folder
1. **Double-click** on the `frontend` folder in File Explorer
2. You should now see the contents of the frontend folder:
   - `package.json`
   - `public` folder
   - `src` folder
   - (and maybe other files)

### Step 2: Right-click INSIDE the folder
1. **Click in the empty white space** (not on any file or folder)
2. **Right-click** in that empty space
3. Now you should see "New" in the menu!

### Step 3: Create the file
1. Hover over **"New"** in the right-click menu
2. Click **"Text Document"**
3. A new file appears: "New Text Document.txt"

### Step 4: Rename to .env
1. **Right-click** on "New Text Document.txt"
2. Click **"Rename"**
3. **Delete everything** and type: `.env`
4. Press Enter
5. Windows warns you - click **"Yes"**

### Step 5: Add content
1. **Double-click** the `.env` file (it will open in Notepad)
2. Type exactly:
   ```
   REACT_APP_API_URL=http://localhost:8000
   ```
3. Press **Ctrl + S** to save
4. Close Notepad

## Alternative: Use the Batch File (Easiest!)

Instead of doing all this manually:

1. Go back to the main project folder (`490deploy`)
2. **Double-click** `create-env.bat`
3. It will create the file automatically!

## Visual Guide

**Wrong:** Right-clicking on the folder icon
```
[frontend] ← Don't right-click here!
```

**Correct:** Open folder, then right-click in empty space
```
frontend/
  ├── package.json
  ├── public/
  ├── src/
  └── [empty space] ← Right-click HERE!
```

