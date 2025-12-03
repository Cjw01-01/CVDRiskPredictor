import sys
import os

# Add paths for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, '../../backend')
sys.path.insert(0, backend_dir)
sys.path.insert(0, current_dir)

# Set model paths - download from HF Hub if not present
models_dir = os.path.join(current_dir, 'models')
os.makedirs(models_dir, exist_ok=True)
os.environ['MODEL_DIR'] = models_dir

# Set model URLs to download from Hugging Face Hub
HF_REPO = os.environ.get('HF_MODEL_REPO', 'carlwakim/cvd-risk-models')
os.environ['HYPERTENSION_MODEL_URL'] = os.environ.get('HYPERTENSION_MODEL_URL', f'https://huggingface.co/{HF_REPO}/resolve/main/hypertension.pt')
os.environ['CIMT_MODEL_URL'] = os.environ.get('CIMT_MODEL_URL', f'https://huggingface.co/{HF_REPO}/resolve/main/cimt_reg.pth')
os.environ['VESSEL_MODEL_URL'] = os.environ.get('VESSEL_MODEL_URL', f'https://huggingface.co/{HF_REPO}/resolve/main/vessel.pth')
os.environ['FUSION_MODEL_URL'] = os.environ.get('FUSION_MODEL_URL', f'https://huggingface.co/{HF_REPO}/resolve/main/fusion_cvd_noskewed.pth')

# Import after path setup
from mangum import Mangum

# Import the FastAPI app
import importlib.util
main_path = os.path.join(backend_dir, "main.py")
spec = importlib.util.spec_from_file_location("main", main_path)
main_module = importlib.util.module_from_spec(spec)
sys.modules["main"] = main_module
spec.loader.exec_module(main_module)
app = main_module.app

# Create the handler for Vercel
mangum_handler = Mangum(app, lifespan="off")

def handler(event, context):
    """Vercel serverless function entry point"""
    try:
        return mangum_handler(event, context)
    except Exception as e:
        import traceback
        return {
            "statusCode": 500,
            "body": f"Function error: {str(e)}\n{traceback.format_exc()}"
        }

