@echo off
REM Script to remove Hugging Face token from git history and push to GitHub

echo ========================================
echo Removing Hugging Face Token from History
echo ========================================
echo.

REM Set non-interactive editor
set GIT_EDITOR=echo
set GIT_SEQUENCE_EDITOR=echo
git config core.editor echo
git config sequence.editor echo

echo Step 1: Creating backup branch...
git branch backup-before-token-removal 2>nul

echo Step 2: Extracting file from old commit...
git show 0d7fb1f:notebooks/deep_fusion_notskewed.ipynb > temp_notebook_old.json

echo Step 3: Replacing token in the file...
powershell -Command "(Get-Content temp_notebook_old.json -Raw) -replace 'PASTE_OLD_HF_TOKEN_HERE', 'YOUR_HUGGINGFACE_TOKEN_HERE' | Set-Content temp_notebook_fixed.json -NoNewline"

echo Step 4: Using git filter-branch to rewrite history...
git filter-branch -f --tree-filter "if exist notebooks\deep_fusion_notskewed.ipynb (powershell -Command \"(Get-Content notebooks\deep_fusion_notskewed.ipynb -Raw) -replace 'PASTE_OLD_HF_TOKEN_HERE', 'YOUR_HUGGINGFACE_TOKEN_HERE' | Set-Content notebooks\deep_fusion_notskewed.ipynb -NoNewline\")" -- --all

echo Step 5: Cleaning up temporary files...
del temp_notebook_old.json 2>nul
del temp_notebook_fixed.json 2>nul

echo.
echo ========================================
echo History cleanup complete!
echo ========================================
echo.
echo You can now push with: git push origin main --force
echo.
pause


