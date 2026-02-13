#!/usr/bin/env python3
"""
Setup verification script - checks all models and dependencies
"""

import os
import sys
from pathlib import Path

def check_dependencies():
    """Check Python package dependencies"""
    print("🔍 Checking Python Dependencies:")
    
    deps = {
        'flask': 'Flask web framework',
        'flask_cors': 'CORS support',
        'transformers': 'Hugging Face transformers',
        'torch': 'PyTorch',
        'fasttext': 'FastText language detection',
        'paddleocr': 'PaddleOCR',
        'cv2': 'OpenCV',
        'numpy': 'NumPy',
        'PIL': 'Pillow'
    }
    
    missing = []
    for dep, desc in deps.items():
        try:
            __import__(dep)
            print(f"  ✅ {dep} - {desc}")
        except ImportError:
            print(f"  ❌ {dep} - {desc}")
            missing.append(dep)
    
    return missing

def check_model_files():
    """Check model files"""
    print("\n🔍 Checking Model Files:")
    
    base_path = Path("models/models")
    
    # FastText
    fasttext_path = base_path / "fasttext" / "lid.176.bin"
    print(f"  {'✅' if fasttext_path.exists() else '❌'} FastText: {fasttext_path}")
    
    # NLLB files
    nllb_files = [
        "pytorch_model.bin",
        "config.json", 
        "tokenizer.json",
        "tokenizer_config.json",
        "sentencepiece.bpe.model",
        "special_tokens_map.json"
    ]
    
    print(f"\n  NLLB Model ({base_path / 'nllb_model'}):")
    missing_nllb = []
    for file in nllb_files:
        path = base_path / "nllb_model" / file
        status = "✅" if path.exists() else "❌"
        print(f"    {status} {file}")
        if not path.exists():
            missing_nllb.append(file)
    
    return missing_nllb

def check_model_loading():
    """Test actual model loading"""
    print("\n🔍 Testing Model Loading:")
    
    try:
        from language_detection.detector import LanguageDetector
        detector = LanguageDetector()
        if detector.model != "fasttext_mock":
            print("  ✅ Language Detection: Real FastText model loaded")
        else:
            print("  ⚠️  Language Detection: Using fallback (script-based)")
    except Exception as e:
        print(f"  ❌ Language Detection: Error - {e}")
    
    try:
        from translation.translator import Translator
        translator = Translator()
        if translator.model != "nllb_mock":
            print("  ✅ Translation: Real NLLB model loaded")
        else:
            print("  ⚠️  Translation: Using fallback (mock responses)")
    except Exception as e:
        print(f"  ❌ Translation: Error - {e}")
    
    try:
        from ocr.ocr_engine import OCREngine
        ocr = OCREngine()
        if ocr.model != "paddleocr_mock":
            print("  ✅ OCR: Real PaddleOCR model loaded")
        else:
            print("  ⚠️  OCR: Using fallback (mock responses)")
    except Exception as e:
        print(f"  ❌ OCR: Error - {e}")

def main():
    print("🚀 Backend Setup Verification")
    print("=" * 50)
    
    # Check dependencies
    missing_deps = check_dependencies()
    
    # Check model files
    missing_files = check_model_files()
    
    # Test model loading
    check_model_loading()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY:")
    
    if not missing_deps and not missing_files:
        print("🎉 All components ready! Backend fully functional.")
        print("\n🚀 Start backend: python app.py")
    else:
        print("⚠️  Some components missing:")
        
        if missing_deps:
            print(f"\n📦 Missing packages: {', '.join(missing_deps)}")
            print("   Fix: pip install " + " ".join(missing_deps))
        
        if missing_files:
            print(f"\n📁 Missing NLLB files: {len(missing_files)} files")
            print("   Fix: Run fix_missing.bat (Windows) or fix_missing.sh (Linux/macOS)")
        
        print("\n🔧 Quick fix: Run the fix_missing script for your platform")
    
    print("\n📚 Documentation:")
    print("   - MISSING.md - Complete missing components list")
    print("   - EXISTING_MODELS.md - Current model status")
    print("   - MODEL_CONFIG.md - Configuration details")

if __name__ == "__main__":
    main()