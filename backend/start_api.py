#!/usr/bin/env python3

import subprocess
import sys
import os

def main():
    print("🚀 Starting Route Optimization API Server...")
    print("=" * 50)
    
    if not os.path.exists("web_api.py"):
        print("❌ Error: web_api.py not found. Please run this script from the backend directory.")
        sys.exit(1)
    
    try:
        import fastapi
        import uvicorn
        print("✅ Dependencies are installed")
    except ImportError:
        print("❌ Missing dependencies. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed")
    
    print("\n📡 API will be available at:")
    print("   - Main API: http://localhost:8000")
    print("   - Interactive Docs: http://localhost:8000/docs")
    print("   - Alternative Docs: http://localhost:8000/redoc")
    print("   - Health Check: http://localhost:8000/health")
    
    print("\n🔗 Available endpoints:")
    print("   - GET  /health          - Health check")
    print("   - GET  /locations       - Get all locations")
    print("   - POST /locations       - Add custom location")
    print("   - POST /optimize        - Optimize route")
    print("   - POST /compare         - Compare routes")
    print("   - POST /visualization   - Get visualization data")
    print("   - POST /street-routing  - Get street routing data")
    print("   - GET  /quick-optimize  - Quick optimization")
    print("   - GET  /stats           - API statistics")
    
    print("\n🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "web_api:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 API server stopped")

if __name__ == "__main__":
    main() 