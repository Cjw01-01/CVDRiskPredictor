"""
Script to copy model files to netlify functions directory for deployment
Run this before deploying to ensure models are available
"""
import shutil
import os

def copy_models():
    """Copy model files from backend to netlify functions directory"""
    backend_dir = os.path.join(os.path.dirname(__file__), '../../backend')
    functions_dir = os.path.dirname(__file__)
    models_dir = os.path.join(functions_dir, 'models')
    
    # Create models directory if it doesn't exist
    os.makedirs(models_dir, exist_ok=True)
    
    model_files = [
        'hypertension.pt',
        'cimt_reg.pth',
        'vessel.pth',
        'fusion_cvd_noskewed.pth'
    ]
    
    copied = []
    for model_file in model_files:
        src = os.path.join(backend_dir, model_file)
        dst = os.path.join(models_dir, model_file)
        
        if os.path.exists(src):
            shutil.copy2(src, dst)
            copied.append(model_file)
            print(f"✓ Copied {model_file}")
        else:
            print(f"✗ Not found: {model_file}")
    
    print(f"\nCopied {len(copied)}/{len(model_files)} model files")
    return copied

if __name__ == '__main__':
    copy_models()


