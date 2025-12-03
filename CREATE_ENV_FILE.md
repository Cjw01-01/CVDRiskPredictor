# How to Create the .env File - Detailed Guide

## Method 1: Using Notepad (Easiest)

### Step 1: Open File Explorer
1. Press `Windows Key + E` to open File Explorer
2. Navigate to:
   ```
   C:\Users\User\OneDrive - American University of Beirut\Desktop\490deploy\frontend
   ```

### Step 2: Create the File
1. **Right-click** in the empty space inside the `frontend` folder
2. Click **New** → **Text Document**
3. A new file called "New Text Document.txt" will appear

### Step 3: Rename the File
1. **Right-click** on "New Text Document.txt"
2. Click **Rename**
3. **Delete everything** and type exactly: `.env`
   - That's: **dot** (.) then **env** (no space, no .txt)
4. Windows will show a warning: "If you change a file name extension, the file might become unusable"
5. Click **Yes**

### Step 4: Add Content
1. **Right-click** on `.env` → **Open with** → **Notepad**
2. **Type this exactly** (no quotes, no spaces):
   ```
   REACT_APP_API_URL=http://localhost:8000
   ```
3. Press **Ctrl + S** to save
4. Close Notepad

### Step 5: Verify
- You should see a file named `.env` in the frontend folder
- It should NOT have `.txt` extension

---

## Method 2: Using Command Prompt (Alternative)

1. **Open Command Prompt**
2. **Run these commands:**

```cmd
cd "C:\Users\User\OneDrive - American University of Beirut\Desktop\490deploy\frontend"
```

```cmd
echo REACT_APP_API_URL=http://localhost:8000 > .env
```

3. **Verify it was created:**
```cmd
dir .env
```

You should see `.env` listed.

---

## Method 3: Using VS Code (If you have it open)

1. In VS Code, go to the `frontend` folder in the file explorer
2. **Right-click** on the `frontend` folder
3. Click **New File**
4. **Type exactly:** `.env`
5. Press Enter
6. **Type the content:**
   ```
   REACT_APP_API_URL=http://localhost:8000
   ```
7. Press **Ctrl + S** to save

---

## Troubleshooting

### Problem: Windows won't let me name it `.env`
**Solution:**
1. Create it as `env.txt` first
2. Then rename to `.env`
3. When Windows warns you, click **Yes**

### Problem: I can't see the file after creating it
**Solution:**
1. In File Explorer, go to **View** tab
2. Check **"File name extensions"** and **"Hidden items"**
3. The `.env` file should now be visible

### Problem: The file still has .txt extension
**Solution:**
1. Make sure "File name extensions" is checked in View tab
2. Right-click → Rename
3. Change from `env.txt` to `.env` (with the dot)
4. Windows will warn you - click **Yes**

### Problem: I'm not sure if I did it right
**Solution:**
1. Right-click on `.env` → **Properties**
2. Check the "Type of file" - it should say "ENV File" or "Text Document"
3. Open it with Notepad to verify the content is:
   ```
   REACT_APP_API_URL=http://localhost:8000
   ```

---

## Visual Guide

**What you should see in the frontend folder:**
```
frontend/
  ├── .env          ← This file (with the dot!)
  ├── package.json
  ├── public/
  └── src/
```

**What the .env file should contain:**
```
REACT_APP_API_URL=http://localhost:8000
```

**Important:**
- No quotes around the URL
- No spaces
- Exactly as shown above
- The file name is `.env` (with dot, no extension)

---

## Quick Check

After creating the file, verify:
1. File name is exactly `.env` (not `env.txt` or `.env.txt`)
2. File contains exactly: `REACT_APP_API_URL=http://localhost:8000`
3. File is in the `frontend` folder (not the root folder)

If all three are correct, you're good to go! ✅

