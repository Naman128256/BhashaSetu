#!/usr/bin/env python3
"""
Install and test ML models for dynamic translation
"""

import subprocess
import sys
import os
from pathlib import Path

def install_package(package):
    """Install a package safely"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ {package} installed successfully")
        return True
    except:
        print(f"X {package} failed to install")
        return False

def test_fasttext():
    """Test FastText installation and model"""
    try:
        import fasttext
        model_path = Path("models/models/fasttext/lid.176.bin")
        if model_path.exists():
            model = fasttext.load_model(str(model_path))
            result = model.predict("नमस्ते", k=1)
            print(f"+ FastText working: {result}")
            return True
        else:
            print("⚠️ FastText model file not found")
            return False
    except Exception as e:
        print(f"❌ FastText test failed: {e}")
        return False

def test_transformers():
    """Test transformers installation"""
    try:
        import transformers
        import torch
        print(f"+ Transformers {transformers.__version__} available")
        print(f"+ PyTorch {torch.__version__} available")
        return True
    except Exception as e:
        print(f"❌ Transformers test failed: {e}")
        return False

def main():
    print("Installing ML packages for dynamic translation...")
    
    # Try to install packages
    packages = [
        "fasttext-wheel",
        "transformers", 
        "torch",
        "sentencepiece"
    ]
    
    for package in packages:
        install_package(package)
    
    print("\n🧪 Testing installations...")
    
    # Test FastText
    fasttext_ok = test_fasttext()
    
    # Test Transformers
    transformers_ok = test_transformers()
    
    print(f"\nResults:")
    print(f"FastText: {'+' if fasttext_ok else 'X'}")
    print(f"Transformers: {'+' if transformers_ok else 'X'}")
    
    if fasttext_ok or transformers_ok:
        print("\n* At least one ML package is working!")
        print("Restart the backend to use real models")
    else:
        print("\n! No ML packages working, will use enhanced mock responses")

if __name__ == "__main__":
    main()