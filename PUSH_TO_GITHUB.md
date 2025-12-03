# Push Project to GitHub

## Repository: https://github.com/Cjw01-01/CVDRiskPredictor.git

### Option 1: Using Git Command Line (if Git is installed)

Open PowerShell or Command Prompt in `C:\cvddeploy` and run:

```bash
# Initialize git repository
git init

# Add remote repository
git remote add origin https://github.com/Cjw01-01/CVDRiskPredictor.git

# Add all files
git add .

# Commit
git commit -m "Initial commit: CVD Risk Predictor with Netlify Functions"

# Push to GitHub
git branch -M main
git push -u origin main
```

### Option 2: Using GitHub Desktop

1. **Download GitHub Desktop**: https://desktop.github.com/
2. **Install and login** with your GitHub account
3. **File → Add Local Repository**
4. **Choose** `C:\cvddeploy`
5. **Publish repository** to `Cjw01-01/CVDRiskPredictor`

### Option 3: Using VS Code / Cursor

1. Open `C:\cvddeploy` in VS Code/Cursor
2. Open Source Control panel (Ctrl+Shift+G)
3. Click "Initialize Repository"
4. Stage all files
5. Commit with message: "Initial commit: CVD Risk Predictor"
6. Click "..." → "Remote" → "Add Remote"
   - Name: `origin`
   - URL: `https://github.com/Cjw01-01/CVDRiskPredictor.git`
7. Click "..." → "Push" → "Push to..."

### What Will Be Pushed:

✅ **Included:**
- All source code (backend, frontend)
- Configuration files (netlify.toml, package.json, etc.)
- Netlify Functions setup
- Documentation files
- Model files in `netlify/functions/models/` (needed for deployment)

❌ **Excluded (via .gitignore):**
- `venv/` (Python virtual environment)
- `node_modules/` (Node dependencies)
- `__pycache__/` (Python cache)
- `.env` files (environment variables)
- Large PDF files
- Duplicate model files in root/backend (only netlify/functions/models/ included)

### After Pushing:

1. Go to https://github.com/Cjw01-01/CVDRiskPredictor
2. Verify all files are there
3. Connect to Netlify for deployment (see DEPLOY_NETLIFY.md)



