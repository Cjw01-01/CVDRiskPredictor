# Deployment Options

## Option 1: Vercel (Recommended - Easiest)

### Setup:
1. Go to https://vercel.com
2. Sign up/login with GitHub
3. Click "New Project"
4. Import your GitHub repo: `Cjw01-01/CVDRiskPredictor`
5. Vercel will auto-detect:
   - Frontend: `frontend/` directory
   - API: `api/` directory (Python functions)
6. Add environment variables (if needed):
   - `HF_MODEL_REPO` = `carlwakim/cvd-risk-models`
7. Click "Deploy"

### Why Vercel:
- ✅ Better Python serverless support than Netlify
- ✅ Auto-detects React + Python
- ✅ Free tier is generous
- ✅ Fast global CDN
- ✅ No configuration needed (uses `vercel.json`)

---

## Option 2: Railway (Full-Stack)

### Setup:
1. Go to https://railway.app
2. Sign up/login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repo: `Cjw01-01/CVDRiskPredictor`
5. Railway will auto-detect and deploy
6. Add environment variables:
   - `HF_MODEL_REPO` = `carlwakim/cvd-risk-models`
7. Railway will give you a URL like: `https://your-app.railway.app`

### Why Railway:
- ✅ Full-stack deployment (frontend + backend together)
- ✅ Docker support
- ✅ $5/month free credit
- ✅ Simple deployment

### Update frontend to use Railway backend:
In Netlify/Vercel frontend, set:
- `REACT_APP_API_URL` = `https://your-app.railway.app`

---

## Option 3: Render (Full-Stack)

### Setup:
1. Go to https://render.com
2. Sign up/login with GitHub
3. Click "New" → "Web Service"
4. Connect your GitHub repo
5. Settings:
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: `Python 3`
6. Add environment variables:
   - `HF_MODEL_REPO` = `carlwakim/cvd-risk-models`
7. Deploy

### Why Render:
- ✅ Free tier available
- ✅ Full-stack support
- ✅ We already tried backend here (had dependency issues, but fixed now)

---

## Option 4: Cloudflare Pages + Workers

### Setup:
1. Go to https://pages.cloudflare.com
2. Connect GitHub repo
3. Build settings:
   - **Framework preset**: React
   - **Build command**: `cd frontend && npm install && npm run build`
   - **Build output directory**: `frontend/build`
4. For backend, use Cloudflare Workers (separate setup)

### Why Cloudflare:
- ✅ Fastest CDN
- ✅ Free tier
- ⚠️ Workers have size limits (might not work for large models)

---

## Recommendation

**Use Vercel** - It's the easiest and most similar to Netlify, but with better Python support.

