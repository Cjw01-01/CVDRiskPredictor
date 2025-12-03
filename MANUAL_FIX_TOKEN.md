# Manual Fix: Remove Hugging Face Token from Git History

## The Problem
GitHub detected a Hugging Face token (`YOUR_HF_TOKEN_HERE`) in a previous commit and is blocking the push.

## Solution Options

### Option 1: Use git-filter-repo (Recommended - Cleanest)

1. **Install git-filter-repo:**
   ```powershell
   pip install git-filter-repo
   ```

2. **Create a replacements file:**
   ```powershell
   echo "PASTE_OLD_HF_TOKEN_HERE==>YOUR_HUGGINGFACE_TOKEN_HERE" > replacements.txt
   ```

3. **Run git-filter-repo:**
   ```powershell
   git filter-repo --replace-text replacements.txt --force
   ```

4. **Push to GitHub:**
   ```powershell
   git push origin main --force
   ```

### Option 2: Use git filter-branch (Alternative)

1. **Open a NEW PowerShell window** (to avoid vim issues)

2. **Run the provided script:**
   ```powershell
   cd C:\cvddeploy
   powershell -ExecutionPolicy Bypass -File fix-git-history-simple.ps1
   ```

3. **If that doesn't work, manually run (substitute your old token string where indicated):**
   ```powershell
   git config core.editor "powershell -Command `"exit 0`""
   git filter-branch -f --tree-filter "powershell -Command `"(Get-Content notebooks/deep_fusion_notskewed.ipynb -Raw) -replace 'PASTE_OLD_HF_TOKEN_HERE', 'YOUR_HUGGINGFACE_TOKEN_HERE' | Set-Content notebooks/deep_fusion_notskewed.ipynb -NoNewline`"" -- --all
   ```

4. **Push to GitHub:**
   ```powershell
   git push origin main --force
   ```

### Option 3: Start Fresh (If above don't work)

1. **Create a new branch without the problematic commit:**
   ```powershell
   git checkout --orphan new-main
   git add .
   git commit -m "Initial commit: CVD Risk Predictor (token removed)"
   git branch -D main
   git branch -m main
   ```

2. **Force push:**
   ```powershell
   git push origin main --force
   ```

## Important Notes

- **Backup first:** The scripts create backup branches automatically
- **Force push required:** After rewriting history, you must use `--force`
- **Revoke the token:** Go to https://huggingface.co/settings/tokens and revoke your old Hugging Face token
- **Generate new token:** Create a new token if you still need Hugging Face access

## Quick Test

After fixing, verify the token string is gone:
```powershell
git log --all --full-history -- notebooks/deep_fusion_notskewed.ipynb | Select-String "YOUR_HF_TOKEN_HERE"
```
Should return nothing if successful.


