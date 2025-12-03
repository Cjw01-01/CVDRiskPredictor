# Deployment Guide

## Quick Start

### Step 1: Prepare Backend

1. **Copy model files to backend:**
   ```bash
   cp hypertension.pt backend/
   cp cimt_reg.pth backend/
   cp vessel.pth backend/
   cp fusion_cvd_noskewed.pth backend/
   ```

2. **Test backend locally:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python main.py
   ```

   Visit http://localhost:8000/docs to see the API documentation.

### Step 2: Deploy Backend (Choose One)

#### Option A: Railway (Recommended - Easiest)

1. Go to https://railway.app
2. Sign up/login with GitHub
3. Click "New Project" > "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect Python
6. Set root directory to `backend`
7. Add environment variable:
   - `CORS_ORIGINS` = `https://your-netlify-site.netlify.app`
8. Deploy!

**Note:** Railway gives you a URL like `https://your-app.railway.app`

#### Option B: Render

1. Go to https://render.com
2. Create new "Web Service"
3. Connect GitHub repo
4. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
   - Root Directory: `backend`
5. Add environment variables
6. Deploy!

### Step 3: Deploy Frontend to Netlify

1. **Build locally first (optional):**
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **Deploy via Netlify:**
   - Go to https://netlify.com
   - Sign up/login
   - Click "Add new site" > "Import an existing project"
   - Connect your GitHub repository
   - Build settings:
     - Base directory: `frontend`
     - Build command: `npm install && npm run build`
     - Publish directory: `frontend/build`
   - Add environment variable:
     - Key: `REACT_APP_API_URL`
     - Value: `https://your-backend-url.com` (from Step 2)
   - Deploy!

3. **Update CORS in backend:**
   - Go to your backend deployment dashboard
   - Add your Netlify URL to CORS origins
   - Or update `backend/main.py`:
     ```python
     allow_origins=["https://your-site.netlify.app"]
     ```

## Testing

1. **Test backend:**
   - Visit `https://your-backend-url.com/docs`
   - Try the `/health` endpoint
   - Test `/predict` with an image

2. **Test frontend:**
   - Visit your Netlify URL
   - Upload a retinal image
   - Select a model
   - Check predictions

## Troubleshooting

### Backend Issues

**Model not loading:**
- Ensure model files are in backend directory
- Check file paths in `main.py`
- Verify PyTorch version compatibility

**CORS errors:**
- Update `allow_origins` in `backend/main.py`
- Add your Netlify URL to allowed origins

**Memory errors:**
- Models might be too large for free tiers
- Consider model optimization or paid hosting

### Frontend Issues

**API connection failed:**
- Check `REACT_APP_API_URL` environment variable
- Verify backend is running
- Check browser console for errors

**Build fails:**
- Run `npm install` in frontend directory
- Check Node.js version (should be 16+)

## Model Architecture Adjustments

If your models have specific architectures, you may need to modify `backend/main.py`:

```python
# Example: If you know the model architecture
class YourModel(nn.Module):
    def __init__(self):
        super().__init__()
        # Define your architecture
        
    def forward(self, x):
        # Define forward pass
        return x

# Then load with:
model = YourModel()
model.load_state_dict(torch.load(model_path, map_location=device))
```

## Cost Considerations

- **Netlify:** Free tier is generous for frontend
- **Railway:** $5/month for hobby plan (includes $5 credit)
- **Render:** Free tier available but slower

## Security Notes

For production:
1. Add authentication to API
2. Rate limiting
3. Input validation
4. Secure CORS origins (not `*`)
5. HTTPS only

