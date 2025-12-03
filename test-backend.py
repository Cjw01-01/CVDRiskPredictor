"""
Quick test script to verify backend is working
Run this after starting the backend server
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    print("Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health check: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_docs():
    """Test that docs are accessible"""
    print("\nTesting API documentation...")
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ API docs accessible at http://localhost:8000/docs")
            return True
        else:
            print(f"❌ Docs returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Docs check failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Backend Connection Test")
    print("=" * 50)
    print(f"\nTesting connection to {BASE_URL}")
    print("Make sure backend is running (python main.py)\n")
    
    health_ok = test_health()
    docs_ok = test_docs()
    
    print("\n" + "=" * 50)
    if health_ok and docs_ok:
        print("✅ Backend is working correctly!")
        print("\nYou can now:")
        print("1. Open http://localhost:8000/docs to see API docs")
        print("2. Start the frontend (npm start in frontend directory)")
    else:
        print("❌ Backend has issues. Check the error messages above.")
    print("=" * 50)

