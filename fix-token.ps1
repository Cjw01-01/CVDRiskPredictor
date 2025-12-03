# Script to remove Hugging Face token from git history (fill in your OLD token string)
$token = "PASTE_OLD_HF_TOKEN_HERE"
$replacement = "YOUR_HUGGINGFACE_TOKEN_HERE"

# Get the file content from the old commit
$content = git show 0d7fb1f:notebooks/deep_fusion_notskewed.ipynb
$content = $content -replace $token, $replacement

# Write to temp file
$tempFile = [System.IO.Path]::GetTempFileName()
$content | Out-File -FilePath $tempFile -Encoding utf8 -NoNewline

# Checkout the old commit
git checkout 0d7fb1f -- notebooks/deep_fusion_notskewed.ipynb

# Replace the content
Copy-Item $tempFile notebooks/deep_fusion_notskewed.ipynb -Force
Remove-Item $tempFile

# Stage the change
git add notebooks/deep_fusion_notskewed.ipynb

# Amend the commit
git commit --amend --no-edit

# Rebase the new commit on top
git rebase --onto HEAD 0d7fb1f main


