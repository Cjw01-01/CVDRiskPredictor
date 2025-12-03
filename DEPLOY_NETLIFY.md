# Netlify Deployment Instructions

## ✅ Setup Complete!

All Netlify Functions have been installed and configured. Here's what was set up:

### Files Created:

1. **`netlify/functions/predict.py`** - Main Netlify Function handler
2. **`netlify/functions/requirements.txt`** - Python dependencies for the function
3. **`netlify/functions/copy_models.py`** - Script to copy model files
4. **`netlify/functions/models/`** - Directory containing all model files (already copied)
5. **`netlify.toml`** - Updated with function configuration
6. **`.netlifyignore`** - Files to exclude from deployment
7. **`package.json`** - Root package.json with build scripts

### How to Deploy:

#### Step 1: Install Netlify CLI (if not already installed)
```bash
npm install -g netlify-cli
```

#### Step 2: Login to Netlify
```bash
netlify login
```

#### Step 3: Initialize Site (first time only)
```bash
netlify init
```
- Choose "Create & configure a new site"
- Choose your team
- Site name (or leave blank for auto-generated)
- Build command: `npm run copy-models && cd frontend && npm install && npm run build`
- Publish directory: `frontend/build`

#### Step 4: Deploy
```bash
# Test deployment first
netlify deploy

# Deploy to production
netlify deploy --prod
```

### Or Deploy via GitHub:

1. Push your code to GitHub
2. Go to [Netlify Dashboard](https://app.netlify.com)
3. Click "Add new site" → "Import an existing project"
4. Connect your GitHub repository
5. Netlify will auto-detect settings from `netlify.toml`
6. Click "Deploy site"

### Important Notes:

⚠️ **Model File Size Warning:**
- Netlify Functions have a 50MB limit per function (free tier)
- Your PyTorch models might exceed this
- If deployment fails due to size:
  1. Consider using Netlify Pro (500MB limit)
  2. Or use a separate backend service (Railway, Render, etc.)

### Environment Variables:

If you need any environment variables, set them in:
- Netlify Dashboard → Site settings → Environment variables

### API Endpoints After Deployment:

- Production: `https://your-site.netlify.app/.netlify/functions/predict`
- Or via redirect: `https://your-site.netlify.app/api/*`

The frontend is already configured to use the Netlify function endpoint in production automatically!

### Testing Locally:

You can test the Netlify function locally:
```bash
netlify dev
```

This will start both the frontend and the Netlify function locally.



