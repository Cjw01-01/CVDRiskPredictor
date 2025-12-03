# Fix: Large Model Files Exceed GitHub Limit

## Problem
Model files are too large for GitHub (100MB limit):
- `cimt_reg.pth`: 318.06 MB
- `hypertension.pt`: 1547.63 MB (1.5 GB!)

## Solution: Remove Models from Git

Run these commands in Git Bash:

```bash
# Remove the large files from git tracking (but keep them locally)
git rm --cached netlify/functions/models/*.pth
git rm --cached netlify/functions/models/*.pt
git rm --cached backend/*.pth
git rm --cached backend/*.pt

# Add the updated .gitignore
git add .gitignore

# Amend the previous commit to remove the large files
git commit --amend -m "Initial commit: CVD Risk Predictor with Netlify Functions setup (models excluded)"

# Force push (since we're amending the first commit)
git push -u origin main --force
```

## Alternative: Use Git LFS (if you need to track models)

If you want to track the models using Git Large File Storage:

```bash
# Install Git LFS (if not installed)
git lfs install

# Track model files with LFS
git lfs track "*.pth"
git lfs track "*.pt"
git add .gitattributes

# Remove from previous commit and re-add with LFS
git rm --cached netlify/functions/models/*.pth
git rm --cached netlify/functions/models/*.pt
git add netlify/functions/models/*.pth
git add netlify/functions/models/*.pt

git commit --amend -m "Initial commit: CVD Risk Predictor with Git LFS for models"
git push -u origin main --force
```

## Recommended: Don't Track Models in Git

**Best practice:** Store models separately (S3, Google Drive, etc.) and download them during deployment.

For Netlify deployment, you can:
1. Store models in a cloud storage (S3, Google Drive, etc.)
2. Download them during Netlify build process
3. Or use Netlify Large Media (Pro feature)



