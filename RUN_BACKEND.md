# How to Run Backend - Exact Commands

## The Problem
The error shows it's trying to open `main.pyser\OneDrive` instead of `main.py`. This is likely a copy-paste issue or path problem.

## Solution: Type the command carefully

In your Command Prompt (where you see `(venv)`), type this **exactly**:

```cmd
python main.py
```

**Important:**
- Type it manually, don't copy-paste
- Make sure there's a space between `python` and `main.py`
- Make sure you're in the backend folder (you should see `backend>` in your prompt)

## Complete Step-by-Step (All Commands)

1. **Open Command Prompt**

2. **Navigate to backend:**
   ```cmd
   cd "C:\Users\User\OneDrive - American University of Beirut\Desktop\490deploy\backend"
   ```

3. **Activate venv:**
   ```cmd
   venv\Scripts\activate.bat
   ```

4. **Install dependencies (if not done):**
   ```cmd
   pip install -r requirements.txt
   ```

5. **Run the server:**
   ```cmd
   python main.py
   ```
   **Type this manually - don't copy paste!**

6. **You should see:**
   ```
   INFO: Uvicorn running on http://0.0.0.0:8000
   ```

## If It Still Doesn't Work

Try this alternative:

```cmd
python .\main.py
```

Or check if the file exists:
```cmd
dir main.py
```

If the file doesn't exist, there's a problem with the setup.

