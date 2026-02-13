#!/usr/bin/env python3
"""
Force load real models and test
"""

import sys
import os
sys.path.append('.')

def test_model_loading():
    """Test if models can load"""
    
    print("Testing model loading...")
    
    # Test transformers
    try:
        import transformers
        import torch
        print(f"+ Transformers {transformers.__version__} available")
        print(f"+ PyTorch {torch.__version__} available")
    except Exception as e:
        print(f"- Transformers/PyTorch error: {e}")
        return False
    
    # Test NLLB model loading
    try:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        
        model_path = "models/models/nllb_model"
        print(f"Loading NLLB from: {model_path}")
        
        tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
        print("+ Tokenizer loaded")
        
        model = AutoModelForSeq2SeqLM.from_pretrained(
            model_path, 
            local_files_only=True,
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True
        )
        print("+ Model loaded")
        
        # Test translation
        text = "hello world"
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_length=50,
                num_beams=2,
                early_stopping=True
            )
        
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"+ Translation test: '{text}' -> '{result}'")
        
        return True
        
    except Exception as e:
        print(f"- NLLB loading error: {e}")
        return False

if __name__ == "__main__":
    success = test_model_loading()
    if success:
        print("\n* Models can load successfully!")
        print("The issue might be in the backend configuration.")
    else:
        print("\n* Models cannot load - using enhanced mock responses.")