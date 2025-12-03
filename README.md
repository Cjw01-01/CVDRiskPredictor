# CVD Risk Predictor - Deployment

A beautiful web application for predicting Cardiovascular Disease (CVD) risk from retinal eye images using deep learning models.

## Features

- **4 Model Options:**
  - Hypertension Detection (Binary Classification: 0 or 1)
  - CIMT Regression (Carotid Intima-Media Thickness: 0.4-1.2)
  - A/V Segmentation (Vessel Masking)
  - Fusion Model (Combined CVD Risk Prediction)

- **Beautiful Modern UI** with gradient design
- **Real-time Predictions** with loading states
- **Image Preview** before prediction
- **Responsive Design** for all devices

## Project Structure

```
.
├── frontend/          # React frontend (deploy to Netlify)
│   ├── src/
│   ├── public/
│   └── package.json
├── backend/          # FastAPI backend (deploy separately)
│   ├── main.py
│   └── requirements.txt
├── *.pth, *.pt      # PyTorch model files
└── README.md
```

## Setup Instructions

### Backend Setup (FastAPI)

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Copy model files to backend directory:**
   ```bash
   cp ../hypertension.pt .
   cp ../cimt_reg.pth .
   cp ../vessel.pth .
   cp ../fusion_cvd_noskewed.pth .
   ```

5. **Run the server:**
   ```bash
   python main.py
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup (React)

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create `.env` file:**
   ```env
   REACT_APP_API_URL=http://localhost:8000
   ```

4. **Run development server:**
   ```bash
   npm start
   ```

   The app will be available at `http://localhost:3000`

## Deployment

### Deploy Backend

You can deploy the FastAPI backend to:
- **Railway** (recommended): https://railway.app
- **Render**: https://render.com
- **Heroku**: https://heroku.com
- **AWS/GCP/Azure**: Any cloud provider

**For Railway:**
1. Create a new project
2. Connect your GitHub repo
3. Set root directory to `backend`
4. Add environment variables if needed
5. Deploy!

**Important:** Update the CORS origins in `backend/main.py` with your frontend URL.

### Deploy Frontend to Netlify

1. **Build the frontend:**
   ```bash
   cd frontend
   npm run build
   ```

2. **Deploy to Netlify:**
   - Go to https://netlify.com
   - Drag and drop the `frontend/build` folder, OR
   - Connect your GitHub repo and set:
     - Build command: `cd frontend && npm install && npm run build`
     - Publish directory: `frontend/build`

3. **Set Environment Variable:**
   - In Netlify dashboard, go to Site settings > Environment variables
   - Add: `REACT_APP_API_URL` = `https://your-backend-url.com`

4. **Update netlify.toml redirects** with your backend URL

## Model Architecture Notes

The current implementation uses generic model loading. You may need to adjust:

1. **Model Architecture:** If your models have specific architectures, you'll need to define them in `backend/main.py` before loading.

2. **Input Size:** Currently set to 224x224. Adjust `target_size` in `preprocess_image()` if your models expect different sizes.

3. **Output Format:** The prediction functions handle common output formats, but you may need to adjust based on your specific model outputs.

## Troubleshooting

### Model Loading Errors

If you get model loading errors:
1. Check that model files are in the backend directory
2. Verify PyTorch version compatibility
3. You may need to define the model architecture before loading

### CORS Errors

Update the CORS origins in `backend/main.py`:
```python
allow_origins=["https://your-netlify-site.netlify.app"]
```

### Image Processing Errors

Ensure images are in supported formats (PNG, JPG, JPEG) and not corrupted.

## License

This project is for educational/research purposes.

## Support

For issues or questions, please check:
- FastAPI docs: https://fastapi.tiangolo.com
- React docs: https://react.dev
- Netlify docs: https://docs.netlify.com

