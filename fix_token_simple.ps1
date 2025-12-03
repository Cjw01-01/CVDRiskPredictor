# Simple PowerShell script to remove token from git history
$ErrorActionPreference = "Stop"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Removing Hugging Face Token from Git History" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Set environment variables
$env:FILTER_BRANCH_SQUELCH_WARNING = "1"
$env:GIT_EDITOR = "echo"
$env:GIT_SEQUENCE_EDITOR = "echo"

# Configure git
git config core.editor echo
git config sequence.editor echo

Write-Host "Creating backup branch..." -ForegroundColor Yellow
git branch backup-before-token-cleanup-ps1 2>$null

Write-Host ""
Write-Host "Rewriting history to remove token..." -ForegroundColor Yellow
Write-Host "This may take a moment..." -ForegroundColor Yellow
Write-Host ""

# The token and replacement (fill in your OLD token string when using)
$token = "PASTE_OLD_HF_TOKEN_HERE"
$replacement = "YOUR_HUGGINGFACE_TOKEN_HERE"

# Create the filter command
$filterCmd = @"
if (Test-Path 'notebooks/deep_fusion_notskewed.ipynb') {
    `$content = Get-Content 'notebooks/deep_fusion_notskewed.ipynb' -Raw -Encoding UTF8
    `$content = `$content -replace '$token', '$replacement'
    Set-Content 'notebooks/deep_fusion_notskewed.ipynb' -Value `$content -NoNewline -Encoding UTF8
}
"@

# Write to a file in current directory
$scriptPath = Join-Path $PWD "temp_token_replace.ps1"
$filterCmd | Out-File -FilePath $scriptPath -Encoding UTF8

try {
    # Run git filter-branch
    $cmd = "git filter-branch -f --tree-filter `"powershell -ExecutionPolicy Bypass -File '$scriptPath'`" -- --all"
    Write-Host "Running: $cmd" -ForegroundColor Gray
    Write-Host ""
    
    $result = Invoke-Expression $cmd 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "============================================================" -ForegroundColor Green
        Write-Host "SUCCESS! History rewritten." -ForegroundColor Green
        Write-Host "============================================================" -ForegroundColor Green
        Write-Host ""
        
        Write-Host "Cleaning up backup refs..." -ForegroundColor Yellow
        git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin 2>$null
        git reflog expire --expire=now --all 2>$null
        git gc --prune=now --aggressive 2>$null
        
        Write-Host ""
        Write-Host "Next step: git push origin main --force" -ForegroundColor Cyan
    } else {
        Write-Host ""
        Write-Host "============================================================" -ForegroundColor Red
        Write-Host "ERROR: Filter-branch failed" -ForegroundColor Red
        Write-Host "============================================================" -ForegroundColor Red
        Write-Host ""
        Write-Host "Output: $result" -ForegroundColor Yellow
        exit 1
    }
} finally {
    # Clean up
    if (Test-Path $scriptPath) {
        Remove-Item $scriptPath -ErrorAction SilentlyContinue
    }
}


