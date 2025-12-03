# Simple script to remove token using git filter-branch
# Run this in a NEW PowerShell window

$ErrorActionPreference = "Stop"

Write-Host "Setting up non-interactive git..." -ForegroundColor Yellow

# Configure git to not use interactive editors
git config core.editor "powershell -Command `"exit 0`""
$env:GIT_EDITOR = "powershell -Command `"exit 0`""
$env:GIT_SEQUENCE_EDITOR = "powershell -Command `"exit 0`""

Write-Host "Creating backup branch..." -ForegroundColor Yellow
git branch backup-before-cleanup-$(Get-Date -Format 'yyyyMMdd-HHmmss') | Out-Null

Write-Host "Rewriting git history to remove token..." -ForegroundColor Yellow
Write-Host "This may take a moment..." -ForegroundColor Yellow

# Use git filter-branch with a PowerShell command
$filterCommand = @"
if (Test-Path 'notebooks/deep_fusion_notskewed.ipynb') {
    `$content = Get-Content 'notebooks/deep_fusion_notskewed.ipynb' -Raw
    `$content = `$content -replace 'PASTE_OLD_HF_TOKEN_HERE', 'YOUR_HUGGINGFACE_TOKEN_HERE'
    Set-Content 'notebooks/deep_fusion_notskewed.ipynb' -Value `$content -NoNewline
}
"@

# Write the filter script to a temp file
$filterScript = [System.IO.Path]::GetTempFileName() + ".ps1"
$filterCommand | Out-File -FilePath $filterScript -Encoding UTF8

try {
    # Run git filter-branch
    $result = git filter-branch -f --tree-filter "powershell -ExecutionPolicy Bypass -File `"$filterScript`"" -- --all 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`nHistory cleanup successful!" -ForegroundColor Green
        Write-Host "`nYou can now push with:" -ForegroundColor Yellow
        Write-Host "  git push origin main --force" -ForegroundColor Cyan
    } else {
        Write-Host "`nError during filter-branch. Output:" -ForegroundColor Red
        Write-Host $result
    }
} finally {
    # Clean up
    Remove-Item $filterScript -ErrorAction SilentlyContinue
}

Write-Host "`nDone!" -ForegroundColor Green


