# Remove Hugging Face token from git history
$ErrorActionPreference = "Stop"

# The token to remove (fill in your OLD token string here when using)
$oldToken = "PASTE_OLD_HF_TOKEN_HERE"
$newToken = "YOUR_HUGGINGFACE_TOKEN_HERE"

Write-Host "Removing token from git history..."

# Get all commits
$commits = git log --oneline --all | ForEach-Object { ($_ -split ' ')[0] }

foreach ($commit in $commits) {
    $fileContent = git show "$commit`:notebooks/deep_fusion_notskewed.ipynb" 2>$null
    if ($fileContent -and $fileContent -match $oldToken) {
        Write-Host "Found token in commit $commit"
        # This would require rewriting the commit, which is complex
    }
}

Write-Host "Note: This requires interactive git commands. Consider using:"
Write-Host "1. GitHub's URL to allow the secret: https://github.com/Cjw01-01/CVDRiskPredictor/security/secret-scanning/unblock-secret/36GDWzqzUFtboN57DySb7hmMl6s"
Write-Host "2. Or install git-filter-repo: pip install git-filter-repo"
Write-Host "   Then run: git filter-repo --replace-text <(echo '$oldToken==>$newToken')"


