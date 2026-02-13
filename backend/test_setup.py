#!/usr/bin/env python3
"""
Quick setup test script to verify backend installation
"""

import sys
import os
import importlib
import logging

def test_python_version():
    """Test Python version"""
    print(f"Python version: {sys.version}")
    if sys.version_info < (3, 10):
        print("❌ Python 3.10+ required")
        return False
    print("✅ Python version OK")
    return True

def test_imports():
    """Test required package imports"""
    required_packages = [
        'flask',
        'flask_cors',
        'cv2',
        'numpy',
        'PIL',
        'werkzeug'
    ]
    
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package} imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import {package}: {e}")
            failed_imports.append(package)
    
    return len(failed_imports) == 0

def test_directories():
    """Test directory structure"""
    required_dirs = [
        'routes',
        'services', 
        'utils',
        'ocr',
        'translation',
        'language_detection',
        'summarizer'
    ]
    
    missing_dirs = []
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✅ Directory {directory} exists")
        else:
            print(f"❌ Directory {directory} missing")
            missing_dirs.append(directory)
    
    return len(missing_dirs) == 0

def test_config():
    """Test configuration loading"""
    try:
        from utils.config import Config
        Config.init_directories()
        print("✅ Configuration loaded successfully")
        print(f"   Host: {Config.HOST}")
        print(f"   Port: {Config.PORT}")
        print(f"   Models dir: {Config.MODELS_DIR}")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_logging():
    """Test logging setup"""
    try:
        from utils.logger import setup_logging, get_logger
        setup_logging()
        logger = get_logger(__name__)
        logger.info("Test log message")
        print("✅ Logging system initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Logging test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🔍 Testing Backend Setup...")
    print("=" * 50)
    
    tests = [
        ("Python Version", test_python_version),
        ("Package Imports", test_imports),
        ("Directory Structure", test_directories),
        ("Configuration", test_config),
        ("Logging System", test_logging)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Testing {test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"   Test failed!")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend setup is ready.")
        print("\n🚀 To start the backend:")
        print("   Windows: start.bat")
        print("   Linux/macOS: ./start.sh")
    else:
        print("❌ Some tests failed. Please check the setup.")
        print("\n🔧 To fix issues:")
        print("   1. Ensure virtual environment is activated")
        print("   2. Run: pip install -r requirements.txt")
        print("   3. Check directory structure")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)