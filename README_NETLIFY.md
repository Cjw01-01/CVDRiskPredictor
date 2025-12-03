# Netlify Deployment Guide

## Setup for Netlify Functions

This project uses Netlify Functions to deploy the FastAPI backend as serverless functions.

### Prerequisites

1. Install Netlify CLI (if deploying locally):
   ```bash
   npm install -g netlify-cli
   ```

2. Ensure all dependencies are installed:
   ```bash
   cd frontend && npm install
   ```

### Before Deploying

1. **Copy model files to Netlify Functions directory:**
   ```bash
   python netlify/functions/copy_models.py
   ```
   
   This copies all model files (`.pt` and `.pth`) from `backend/` to `netlify/functions/models/`

### Deployment

#### Option 1: Deploy via Netlify Dashboard

1. Connect your GitHub repository to Netlify
2. Set build command: `npm run build`
3. Set publish directory: `frontend/build`
4. Netlify will automatically detect the `netlify.toml` configuration

#### Option 2: Deploy via Netlify CLI

```bash
# Login to Netlify
netlify login

# Initialize site (first time only)
netlify init

# Deploy
netlify deploy --prod
```

### Important Notes

⚠️ **Model File Size**: PyTorch model files are large. Netlify Functions have:
- 50MB limit per function (free tier)
- 500MB limit (Pro tier)

If your models exceed this, consider:
1. Using Netlify Large Media
2. Storing models in S3/Cloud Storage and downloading on function cold start
3. Using a separate backend service (Railway, Render, etc.)

### Environment Variables

If needed, set environment variables in Netlify Dashboard:
- Go to Site settings → Environment variables
- Add any required variables

### Function Endpoints

After deployment, your API will be available at:
- `https://your-site.netlify.app/.netlify/functions/predict`
- Or via redirect: `https://your-site.netlify.app/api/*`

### Troubleshooting

1. **Function timeout**: Increase timeout in `netlify.toml` (max 26s for free, 50s for Pro)
2. **Model not found**: Ensure `copy_models.py` was run before deployment
3. **Import errors**: Check that all dependencies are in `netlify/functions/requirements.txt`



