#!/usr/bin/env python3
"""
Minimal startup script that works with Python 3.13
"""

import subprocess
import sys
import os
from pathlib import Path

def install_package(package):
    """Install a package, ignore errors"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed")
        return True
    except:
        print(f"⚠️  {package} failed to install")
        return False

def main():
    print("🚀 Minimal Backend Setup")
    print("=" * 30)
    
    # Install essential packages
    essential = ["Flask", "Flask-CORS", "Werkzeug", "numpy", "Pillow", "requests"]
    
    print("Installing essential packages...")
    for package in essential:
        install_package(package)
    
    # Try optional packages
    optional = ["transformers", "torch", "fasttext-wheel", "paddleocr"]
    
    print("\nTrying optional packages...")
    for package in optional:
        install_package(package)
    
    # Create directories
    print("\nCreating directories...")
    Path("logs").mkdir(exist_ok=True)
    Path("temp").mkdir(exist_ok=True)
    print("✅ Directories created")
    
    # Start backend
    print("\n🚀 Starting backend...")
    try:
        import app
        app.create_app().run(host='127.0.0.1', port=5005, debug=False)
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")

if __name__ == "__main__":
    main()