import sys
import os

# Add paths for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, '../../backend')
sys.path.insert(0, backend_dir)
sys.path.insert(0, current_dir)

# Set model paths to use models in functions directory
models_dir = os.path.join(current_dir, 'models')
if os.path.exists(models_dir):
    # Update model paths to use local models directory
    os.environ['MODEL_DIR'] = models_dir

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

# Create the handler for Netlify Functions
handler = Mangum(app, lifespan="off")

def lambda_handler(event, context):
    """Netlify Functions entry point"""
    return handler(event, context)

