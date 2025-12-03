"""
Hugging Face Space entry point.
This serves the FastAPI backend which handles both API and static frontend.
"""
import uvicorn
import os

# Set port from environment (HF Spaces provides this)
port = int(os.environ.get("PORT", 7860))

if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )

