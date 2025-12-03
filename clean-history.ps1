# Script to remove Hugging Face token from git history
$ErrorActionPreference = "Stop"

Write-Host "Starting history cleanup..."

# Set git to use a non-interactive editor
$env:GIT_EDITOR = "powershell -Command `"exit 0`""
$env:GIT_SEQUENCE_EDITOR = "powershell -Command `"exit 0`""

# The token to replace (fill in your OLD token string when using this script)
$oldToken = 'PASTE_OLD_HF_TOKEN_HERE'
$newToken = 'YOUR_HUGGINGFACE_TOKEN_HERE'

# Get current branch
$currentBranch = git rev-parse --abbrev-ref HEAD
Write-Host "Current branch: $currentBranch"

# Create a backup branch first
Write-Host "Creating backup branch..."
git branch backup-before-cleanup 2>&1 | Out-Null

# Method: Use git filter-branch with tree-filter
Write-Host "Rewriting history to remove token..."

# Create a temp script for the replacement
$replaceScript = @"
`$content = Get-Content 'notebooks/deep_fusion_notskewed.ipynb' -Raw
`$content = `$content -replace 'PASTE_OLD_HF_TOKEN_HERE', 'YOUR_HUGGINGFACE_TOKEN_HERE'
Set-Content 'notebooks/deep_fusion_notskewed.ipynb' -Value `$content -NoNewline
"@

$replaceScript | Out-File -FilePath "temp-replace.ps1" -Encoding UTF8

# Use git filter-branch
git filter-branch -f --tree-filter "powershell -ExecutionPolicy Bypass -File temp-replace.ps1" -- --all

# Clean up
Remove-Item "temp-replace.ps1" -ErrorAction SilentlyContinue

Write-Host "History cleanup complete!"
Write-Host "You can now push with: git push origin $currentBranch --force"


