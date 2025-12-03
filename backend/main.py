from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import torch
import torch.nn as nn
from PIL import Image
import io
import numpy as np
from typing import Optional, Union
import base64
import timm
import os
import urllib.request

app = FastAPI(title="CVD Risk Predictor API")

# Add CORS headers to all responses (workaround for HF Spaces)
@app.middleware("http")
async def add_cors_header(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

# Serve static frontend files (for Hugging Face Space deployment)
static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.exists(static_dir):
    # Mount static files
    app.mount("/static", StaticFiles(directory=os.path.join(static_dir, "static")), name="static")
    # Serve index.html for root and all non-API routes
    @app.get("/")
    async def serve_index():
        index_path = os.path.join(static_dir, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"error": "Frontend not found"}
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # Don't intercept API routes
        if full_path.startswith("api") or full_path.startswith("predict") or full_path.startswith("health"):
            raise HTTPException(status_code=404, detail="Not found")
        # Serve index.html for React Router
        index_path = os.path.join(static_dir, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        raise HTTPException(status_code=404, detail="Frontend not found")

# CORS middleware - Allow all origins for public API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=False,  # Must be False when using "*"
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model paths - check for Netlify Functions / custom MODEL_DIR environment
MODEL_DIR = os.environ.get('MODEL_DIR', '')
if MODEL_DIR:
    MODEL_PATHS = {
        'hypertension': os.path.join(MODEL_DIR, 'hypertension.pt'),
        'cimt': os.path.join(MODEL_DIR, 'cimt_reg.pth'),
        'vessel': os.path.join(MODEL_DIR, 'vessel.pth'),
        'fusion': os.path.join(MODEL_DIR, 'fusion_cvd_noskewed.pth'),
    }
else:
    MODEL_PATHS = {
        'hypertension': 'hypertension.pt',
        'cimt': 'cimt_reg.pth',
        'vessel': 'vessel.pth',
        'fusion': 'fusion_cvd_noskewed.pth',
    }

# Model URLs - default to Hugging Face Hub, can be overridden via env vars
HF_REPO = os.environ.get('HF_MODEL_REPO', 'carlwakim/cvd-risk-models')
MODEL_URLS = {
    'hypertension': os.environ.get('HYPERTENSION_MODEL_URL', f'https://huggingface.co/{HF_REPO}/resolve/main/hypertension.pt'),
    'cimt': os.environ.get('CIMT_MODEL_URL', f'https://huggingface.co/{HF_REPO}/resolve/main/cimt_reg.pth'),
    'vessel': os.environ.get('VESSEL_MODEL_URL', f'https://huggingface.co/{HF_REPO}/resolve/main/vessel.pth'),
    'fusion': os.environ.get('FUSION_MODEL_URL', f'https://huggingface.co/{HF_REPO}/resolve/main/fusion_cvd_noskewed.pth'),
}

# Global model storage
models = {}


def ensure_model_file(model_name: str) -> str:
    """
    Ensure the model file exists locally.
    - If it exists on disk: return the path.
    - If not, and a MODEL_URL is configured: download it once.
    """
    model_path = MODEL_PATHS.get(model_name)
    if not model_path:
        raise ValueError(f"Unknown model: {model_name}")

    # Already present
    if os.path.exists(model_path):
        return model_path

    # No URL configured – cannot auto-download
    url = MODEL_URLS.get(model_name)
    if not url:
        raise RuntimeError(
            f"Model file '{model_path}' is missing and no URL is configured.\n"
            f"Set environment variable for this model (e.g. HYPERTENSION_MODEL_URL) "
            f"or mount the file into the container."
        )

    # Make sure directory exists
    os.makedirs(os.path.dirname(model_path) or ".", exist_ok=True)

    # Download the file
    try:
        print(f"Downloading model '{model_name}' from {url} ...")
        with urllib.request.urlopen(url) as response, open(model_path, "wb") as out_file:
            out_file.write(response.read())
        print(f"Downloaded model '{model_name}' to {model_path}")
    except Exception as e:
        raise RuntimeError(f"Failed to download model '{model_name}' from {url}: {e}")

    return model_path


# ==================== MODEL ARCHITECTURES ====================

class RETFoundClassifier(nn.Module):
    """Hypertension classification model using RETFound backbone"""
    def __init__(self, dropout=0.65):
        super().__init__()
        self.backbone = timm.create_model(
            "vit_large_patch16_224",
            pretrained=False,
            num_classes=0,
            global_pool='token',  # Changed to match fusion notebook
        )
        embed_dim = self.backbone.num_features  # 1024

        # Classifier head (simplified for fusion)
        self.head = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(embed_dim, 1)
        )

    def forward(self, x, return_embedding=False):
        features = self.backbone(x)
        logits = self.head(features)
        
        if return_embedding:
            return logits, features
        return logits


class UNet(nn.Module):
    """U-Net for vessel segmentation"""
    def __init__(self, in_ch=3, out_ch=1):
        super().__init__()
        def CBR(in_channels, out_channels):
            return nn.Sequential(
                nn.Conv2d(in_channels, out_channels, 3, padding=1),
                nn.BatchNorm2d(out_channels),
                nn.ReLU(inplace=True)
            )
        self.enc1 = CBR(in_ch, 64)
        self.enc2 = CBR(64, 128)
        self.enc3 = CBR(128, 256)
        self.pool = nn.MaxPool2d(2)
        self.up = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
        self.dec3 = CBR(256+128, 128)
        self.dec2 = CBR(128+64, 64)
        self.final = nn.Conv2d(64, out_ch, 1)

    def forward(self, x, return_features=False):
        e1 = self.enc1(x)
        e2 = self.enc2(self.pool(e1))
        e3 = self.enc3(self.pool(e2))
        
        if return_features:
            # Return learned features from encoder (256 dim after pooling)
            features = torch.nn.functional.adaptive_avg_pool2d(e3, (1, 1)).flatten(1)
            return features
        
        d3 = self.up(e3)
        d3 = self.dec3(torch.cat([d3, e2], dim=1))
        d2 = self.up(d3)
        d2 = self.dec2(torch.cat([d2, e1], dim=1))
        return self.final(d2)


class SiameseMultimodalCIMTRegression(nn.Module):
    """Siamese multimodal model for CIMT regression"""
    def __init__(self):
        super().__init__()
        MODEL_NAME = "seresnext50_32x4d"
        USE_PRETRAINED = True
        CLINICAL_INPUT_DIM = 3  # age + gender (2)
        CLINICAL_HIDDEN_DIM = 128
        BACKBONE_OUTPUT_DIM = 2048
        FUSION_HIDDEN_DIMS = [512, 128]
        DROPOUT_RATE = 0.5

        # Shared backbone for both eyes
        self.backbone = timm.create_model(
            MODEL_NAME,
            pretrained=USE_PRETRAINED,
            num_classes=0,  # Remove classification head
            global_pool='avg'
        )

        # Clinical feature processor
        self.clinical_fc = nn.Sequential(
            nn.Linear(CLINICAL_INPUT_DIM, CLINICAL_HIDDEN_DIM),
            nn.ReLU(),
            nn.Dropout(DROPOUT_RATE)
        )

        # Fusion layers
        fusion_input_dim = BACKBONE_OUTPUT_DIM * 2 + CLINICAL_HIDDEN_DIM

        layers = []
        in_dim = fusion_input_dim
        for hidden_dim in FUSION_HIDDEN_DIMS:
            layers.extend([
                nn.Linear(in_dim, hidden_dim),
                nn.ReLU(),
                nn.Dropout(DROPOUT_RATE)
            ])
            in_dim = hidden_dim

        # Final regression head: outputs 1 scalar, no activation
        layers.append(nn.Linear(in_dim, 1))
        self.fusion = nn.Sequential(*layers)

    def forward(self, left_img, right_img, clinical, return_embedding=False):
        # Extract features from both eyes (shared weights)
        left_features = self.backbone(left_img)
        right_features = self.backbone(right_img)

        # Concatenate bilateral features
        bilateral_features = torch.cat([left_features, right_features], dim=1)

        # Process clinical features
        clinical_features = self.clinical_fc(clinical)

        # Fuse all features
        fused = torch.cat([bilateral_features, clinical_features], dim=1)

        if return_embedding:
            # Return embedding before final layer (128 dim)
            embedding = fused
            for layer in self.fusion[:-1]:
                embedding = layer(embedding)
            prediction = self.fusion[-1](embedding)
            return prediction, embedding

        # Regression output (no sigmoid, pure linear output)
        output = self.fusion(fused)  # Shape: [batch_size, 1]

        return output


class FusionMetaClassifier(nn.Module):
    """Fusion meta-classifier that combines features from HTN, CIMT, and Vessel models"""
    def __init__(self, input_dim=1425, hidden_dims=[512, 256], dropout=0.3):
        super().__init__()

        layers = []
        in_dim = input_dim

        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(in_dim, hidden_dim),
                nn.ReLU(),
                nn.Dropout(dropout)
            ])
            in_dim = hidden_dim

        layers.append(nn.Linear(in_dim, 1))
        self.mlp = nn.Sequential(*layers)

    def forward(self, x):
        return self.mlp(x)


# ==================== MODEL LOADING ====================

def load_model(model_name: str):
    """Load a PyTorch model"""
    if model_name in models:
        return models[model_name]
    
    # Ensure the model file exists locally (download if needed in cloud)
    model_path = ensure_model_file(model_name)
    
    try:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Load checkpoint
        try:
            loaded_data = torch.load(model_path, map_location=device, weights_only=False)
        except TypeError:
            loaded_data = torch.load(model_path, map_location=device)
        
        # Check if it's a state dict or full model
        if isinstance(loaded_data, dict):
            # Check if it's a checkpoint dict or just state_dict
            # Try common checkpoint keys in order
            state_dict = None
            for key in ['model_state_dict', 'model', 'state_dict', 'weights']:
                if key in loaded_data and isinstance(loaded_data[key], dict):
                    state_dict = loaded_data[key]
                    break
            
            # If no checkpoint key found, assume it's a direct state_dict
            if state_dict is None:
                state_dict = loaded_data
            
            # Create model instance based on model_name
            if model_name == 'hypertension':
                model = RETFoundClassifier(dropout=0.65).to(device)
            elif model_name == 'vessel':
                model = UNet(in_ch=3, out_ch=1).to(device)
            elif model_name == 'cimt':
                model = SiameseMultimodalCIMTRegression().to(device)
            elif model_name == 'fusion':
                # Fusion model is a FusionMetaClassifier
                model = FusionMetaClassifier(
                    input_dim=1425,
                    hidden_dims=[512, 256],
                    dropout=0.3
                ).to(device)
            else:
                raise ValueError(f"Unknown model architecture for {model_name}")
            
            # Load state dict
            try:
                model.load_state_dict(state_dict, strict=False)
            except Exception as e:
                print(f"Warning: Could not load all weights strictly: {e}")
                # Try non-strict loading
                model.load_state_dict(state_dict, strict=False)
            
            model.eval()
            models[model_name] = model
            return model
        else:
            # It's a full model object
            model = loaded_data
            model.eval()
            model.to(device)
            models[model_name] = model
            return model
    except Exception as e:
        raise Exception(f"Error loading model {model_name}: {str(e)}")


# ==================== IMAGE PREPROCESSING ====================

def preprocess_image(image: Image.Image, target_size: tuple = (224, 224)) -> torch.Tensor:
    """Preprocess image for model input"""
    # Resize image
    image = image.resize(target_size, Image.BICUBIC)

    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Convert to numpy array and normalize (force float32)
    img_array = np.array(image).astype(np.float32) / 255.0

    # Normalize to ImageNet stats (also float32)
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    img_array = (img_array - mean) / std

    # Convert to tensor **float32** and add batch dimension
    img_tensor = (
        torch.from_numpy(img_array)
        .permute(2, 0, 1)   # HWC ? CHW
        .unsqueeze(0)      # add batch
        .float()           # VERY IMPORTANT: make sure it's float32
    )

    return img_tensor

def preprocess_image_512(image: Image.Image) -> torch.Tensor:
    """Preprocess image for vessel segmentation (512x512)"""
    # Resize to 512x512
    image = image.resize((512, 512), Image.BICUBIC)

    # Ensure RGB
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Convert to float32 in [0, 1]
    img_array = np.array(image).astype(np.float32) / 255.0

    # Convert to CHW tensor, add batch dim, ensure float32
    img_tensor = (
        torch.from_numpy(img_array)
        .permute(2, 0, 1)
        .unsqueeze(0)
        .float()
    )

    return img_tensor


# ==================== PREDICTION FUNCTIONS ====================

def predict_hypertension(model, image_tensor):
    """Predict hypertension (binary classification)"""
    device = next(model.parameters()).device
    image_tensor = image_tensor.to(device)
    
    with torch.no_grad():
        output = model(image_tensor)
        
        # Handle different output formats
        if isinstance(output, (list, tuple)):
            output = output[0]
        
        # Get prediction (0 or 1)
        # Output is logits, apply sigmoid
        prob = torch.sigmoid(output).item()
        prediction = 1 if prob > 0.5 else 0
        confidence = prob if prediction == 1 else 1 - prob
        
        return int(prediction), float(confidence)


def predict_cimt(model, left_img_tensor, right_img_tensor):
    """Predict CIMT (regression) - requires left and right eye images"""
    device = next(model.parameters()).device
    left_img = left_img_tensor.to(device)
    right_img = right_img_tensor.to(device)
    
    # Create dummy clinical features (age normalized, gender)
    # Using default values: age_norm=0.5 (middle age), gender=[0.5, 0.5] (neutral)
    clinical = torch.tensor([[0.5, 0.5, 0.5]], dtype=torch.float32).to(device)
    
    with torch.no_grad():
        output = model(left_img, right_img, clinical)
        
        # Handle different output formats
        if isinstance(output, (list, tuple)):
            output = output[0]
        
        # Get regression value
        value = output.item() if output.numel() == 1 else output[0].item()
        
        # Clamp to expected range (0.4 to 1.2)
        value = max(0.4, min(1.2, value))
        
        return float(value)


def predict_vessel(model, image_tensor, original_image):
    """Predict vessel segmentation and handcrafted features.

    Returns:
        masked_image_b64: PNG of binary vessel mask (0/255) resized to original image size.
        features: dict of simple handcrafted statistics derived from the soft vessel mask.
    """
    device = next(model.parameters()).device
    image_tensor = image_tensor.to(device)

    with torch.no_grad():
        output = model(image_tensor)

        # Handle different output formats
        if isinstance(output, (list, tuple)):
            output = output[0]

        # Soft mask probabilities in [0, 1]
        prob_mask = torch.sigmoid(output).cpu().numpy()[0, 0]

        # Get binary segmentation mask (single channel, 0 or 255) for visualization
        mask = (prob_mask > 0.5).astype(np.uint8) * 255

        # Resize mask to original image size
        mask_pil = Image.fromarray(mask, mode='L')
        mask_pil = mask_pil.resize(original_image.size, Image.NEAREST)

        # Return the mask itself (white vessels on black background) as PNG
        buffer = io.BytesIO()
        mask_pil.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()

        # Handcrafted features similar to those used in fusion (15 values total)
        flat = prob_mask.flatten()
        vessel_density = float(flat.mean())
        vessel_std = float(flat.std())
        percentiles = np.percentile(flat, np.linspace(0, 100, 13)).astype(np.float32)

        feature_names = [
            "vessel_density",
            "vessel_std",
        ] + [f"percentile_{int(p)}" for p in np.linspace(0, 100, 13)]

        feature_values = [vessel_density, vessel_std] + [float(p) for p in percentiles.tolist()]
        features = dict(zip(feature_names, feature_values))

        return img_str, features

def predict_fusion(left_img_tensor, right_img_tensor, htn_model, cimt_model, vessel_model, fusion_model):
    """
    Predict using fusion model by extracting features from all three base models.
    
    Features extracted:
    - HTN: 1 prob + 1024 embedding = 1025
    - CIMT: 1 pred + 128 embedding = 129
    - Vessel: 256 learned + 15 handcrafted (simplified) = 271
    Total: 1425 features
    """
    device = next(fusion_model.parameters()).device
    
    # Preprocess for different models
    # HTN uses left eye image (224x224)
    htn_tensor = left_img_tensor.to(device)
    
    # CIMT uses both left and right eye images (224x224)
    left_cimt = torch.nn.functional.interpolate(
        left_img_tensor, size=(224, 224), mode='bilinear', align_corners=False
    ).to(device)
    right_cimt = torch.nn.functional.interpolate(
        right_img_tensor, size=(224, 224), mode='bilinear', align_corners=False
    ).to(device)
    
    # Vessel uses left eye image (512x512)
    vessel_tensor = torch.nn.functional.interpolate(
        left_img_tensor, size=(512, 512), mode='bilinear', align_corners=False
    ).to(device)
    
    with torch.no_grad():
        # 1. Extract HTN features (1025 dim: 1 prob + 1024 embedding)
        htn_logits, htn_embedding = htn_model(htn_tensor, return_embedding=True)
        htn_prob = torch.sigmoid(htn_logits).cpu().numpy()[0, 0]
        htn_emb = htn_embedding.cpu().numpy()[0]
        htn_features = np.concatenate([[htn_prob], htn_emb])  # 1025 dim
        
        # 2. Extract CIMT features (129 dim: 1 pred + 128 embedding)
        # Use both left and right eye images with dummy clinical features
        clinical = torch.tensor([[0.5, 0.5, 0.5]], dtype=torch.float32).to(device)
        
        cimt_pred, cimt_embedding = cimt_model(left_cimt, right_cimt, clinical, return_embedding=True)
        cimt_pred_val = cimt_pred.cpu().numpy()[0, 0]
        cimt_emb = cimt_embedding.cpu().numpy()[0]
        cimt_features = np.concatenate([[cimt_pred_val], cimt_emb])  # 129 dim
        
        # 3. Extract Vessel features (271 dim: 256 learned + 15 handcrafted)
        vessel_learned = vessel_model(vessel_tensor, return_features=True).cpu().numpy()[0]  # 256 dim
        
        # Simplified handcrafted features (15 dim) - using zeros for now
        # In production, you'd extract these from the vessel mask
        vessel_handcrafted = np.zeros(15, dtype=np.float32)
        
        # Get vessel mask for basic feature extraction
        vessel_mask = vessel_model(vessel_tensor, return_features=False)
        vessel_mask_np = torch.sigmoid(vessel_mask).cpu().numpy()[0, 0]
        
        # Extract basic handcrafted features (simplified version)
        vessel_handcrafted[0] = vessel_mask_np.mean()  # vessel_density
        vessel_handcrafted[1] = vessel_mask_np.std()  # texture_variance (simplified)
        # Fill rest with basic stats
        vessel_handcrafted[2:15] = np.percentile(vessel_mask_np.flatten(), 
                                                 np.linspace(0, 100, 13))
        
        vessel_features = np.concatenate([vessel_learned, vessel_handcrafted])  # 271 dim
        
        # 4. Combine all features (1425 dim total)
        fusion_features = np.concatenate([
            htn_features,    # 1025
            cimt_features,    # 129
            vessel_features   # 271
        ]).astype(np.float32)
        
        # 5. Normalize features (using simple normalization)
        # In production, you'd use the same normalization as training
        fusion_features = (fusion_features - fusion_features.mean()) / (fusion_features.std() + 1e-8)
        
        # 6. Run fusion model
        fusion_tensor = torch.from_numpy(fusion_features).unsqueeze(0).to(device)
        fusion_output = fusion_model(fusion_tensor)
        fusion_prob = torch.sigmoid(fusion_output).item()
        fusion_pred = 1 if fusion_prob > 0.5 else 0
        
        return {
            'prediction': fusion_pred,
            'probability': float(fusion_prob),
            'components': {
                'hypertension': int(htn_pred) if (htn_pred := 1 if htn_prob > 0.5 else 0) else 0,
                'cimt': float(cimt_pred_val),
                'vessel_density': float(vessel_handcrafted[0])
            }
        }


# ==================== API ENDPOINTS ====================

@app.get("/")
def read_root():
    return {"message": "CVD Risk Predictor API", "status": "running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/predict")
async def predict(
    request: Request,
    model: str = Form(...)
):
    """Predict CVD risk using selected model
    
    For hypertension and vessel: requires 'image' (single eye)
    For cimt and fusion: requires 'left_image' and 'right_image' (both eyes)
    """
    
    if model not in MODEL_PATHS:
        raise HTTPException(status_code=400, detail=f"Invalid model: {model}")
    
    try:
        print(f"\n{'='*50}")
        print(f"PREDICTION REQUEST RECEIVED")
        print(f"Model: {model}")
        print(f"{'='*50}\n")
        
        # Parse form data manually to handle optional files
        form = await request.form()
        
        # Determine which models need 2 images vs 1 image
        needs_two_images = model in ['cimt', 'fusion']
        
        if needs_two_images:
            # CIMT and Fusion require both left and right eye images
            if 'left_image' not in form or 'right_image' not in form:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Model '{model}' requires both left_image and right_image"
                )
            
            left_image = form['left_image']
            right_image = form['right_image']
            
            if not hasattr(left_image, 'filename') or not hasattr(right_image, 'filename'):
                raise HTTPException(
                    status_code=400, 
                    detail=f"Model '{model}' requires both left_image and right_image files"
                )
            
            print(f"Left Image: {left_image.filename}")
            print(f"Right Image: {right_image.filename}")
            
            # Read and process both images
            left_bytes = await left_image.read()
            right_bytes = await right_image.read()
            
            left_pil = Image.open(io.BytesIO(left_bytes))
            right_pil = Image.open(io.BytesIO(right_bytes))
            
            # Preprocess both images
            if model == 'cimt':
                left_tensor = preprocess_image_512(left_pil)
                right_tensor = preprocess_image_512(right_pil)
            else:  # fusion
                left_tensor = preprocess_image(left_pil, target_size=(224, 224))
                right_tensor = preprocess_image(right_pil, target_size=(224, 224))
            
        else:
            # Hypertension and Vessel require single image
            if 'image' not in form:
                raise HTTPException(
                    status_code=400,
                    detail=f"Model '{model}' requires 'image' parameter"
                )
            
            image = form['image']
            
            if not hasattr(image, 'filename'):
                raise HTTPException(
                    status_code=400,
                    detail=f"Model '{model}' requires a valid image file"
                )
            
            print(f"Image: {image.filename}")
            
            # Read and process single image
            image_bytes = await image.read()
            image_pil = Image.open(io.BytesIO(image_bytes))
            original_image = image_pil.copy()
            
            # Preprocess image based on model type
            if model == 'vessel':
                image_tensor = preprocess_image_512(image_pil)
            else:  # hypertension
                image_tensor = preprocess_image(image_pil, target_size=(224, 224))
        
        # Load model
        try:
            model_obj = load_model(model)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Model loading error: {str(e)}")
        
        # Make prediction based on model type
        if model == 'hypertension':
            prediction, confidence = predict_hypertension(model_obj, image_tensor)
            return {
                'prediction': prediction,
                'confidence': confidence
            }
        
        elif model == 'cimt':
            value = predict_cimt(model_obj, left_tensor, right_tensor)
            return {
                'prediction': value,
                'value': value
            }
        
        elif model == 'vessel':
            masked_image, vessel_features = predict_vessel(model_obj, image_tensor, original_image)
            return {
                'masked_image': masked_image,
                'features': vessel_features
            }
        
        elif model == 'fusion':
            # Fusion model needs all three base models
            htn_model = load_model('hypertension')
            cimt_model = load_model('cimt')
            vessel_model = load_model('vessel')
            result = predict_fusion(left_tensor, right_tensor, htn_model, cimt_model, vessel_model, model_obj)
            return result
        
        else:
            raise HTTPException(status_code=400, detail="Unknown model type")
    
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"\n{'='*50}")
        print(f"ERROR OCCURRED!")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {str(e)}")
        print(f"\nFull Traceback:")
        print(error_traceback)
        print(f"{'='*50}\n")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
