@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo Removing Hugging Face Token from Git History
echo ============================================================
echo.

REM Set environment variables to suppress warnings and use non-interactive editor
set FILTER_BRANCH_SQUELCH_WARNING=1
set GIT_EDITOR=echo
set GIT_SEQUENCE_EDITOR=echo

REM Configure git
git config core.editor echo
git config sequence.editor echo

echo Creating backup branch...
git branch backup-before-token-cleanup-manual 2>nul

echo.
echo Rewriting history to remove token...
echo This may take a moment...
echo.

REM Use git filter-branch with inline PowerShell command (fill in your OLD token string where indicated)
git filter-branch -f --tree-filter "powershell -Command \"if (Test-Path 'notebooks/deep_fusion_notskewed.ipynb') { $content = Get-Content 'notebooks/deep_fusion_notskewed.ipynb' -Raw -Encoding UTF8; $content = $content -replace 'PASTE_OLD_HF_TOKEN_HERE', 'YOUR_HUGGINGFACE_TOKEN_HERE'; Set-Content 'notebooks/deep_fusion_notskewed.ipynb' -Value $content -NoNewline -Encoding UTF8 }\" " -- --all

if %errorlevel% == 0 (
    echo.
    echo ============================================================
    echo SUCCESS! History rewritten.
    echo ============================================================
    echo.
    echo Cleaning up backup refs...
    git for-each-ref --format="delete %%^(refname^)" refs/original | git update-ref --stdin 2>nul
    git reflog expire --expire=now --all 2>nul
    git gc --prune=now --aggressive 2>nul
    echo.
    echo Next step: git push origin main --force
) else (
    echo.
    echo ============================================================
    echo ERROR: Filter-branch failed
    echo ============================================================
    echo.
    echo You may need to try a different approach.
    echo See MANUAL_FIX_TOKEN.md for alternatives.
)

pause


