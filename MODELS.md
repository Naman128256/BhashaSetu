# ML Models Guide - Nepali & Sinhala Literature Translator

This document provides comprehensive information about all machine learning models used in the backend, including download links, installation instructions, and configuration details.

## Overview

The backend uses 4 main types of ML models for the complete translation pipeline:

1. **OCR Model** - Text extraction from images/PDFs
2. **Translation Model** - Neural machine translation
3. **Language Detection Model** - Automatic language identification
4. **LLM Model** - Post-processing and summarization

---

## 1. OCR Model (PaddleOCR)

### Model Information
- **Framework**: PaddleOCR
- **Purpose**: Optical Character Recognition for Nepali, Sinhala, and English text
- **Size**: ~200-400 MB
- **Languages Supported**: Nepali (Devanagari), Sinhala, English, 80+ languages

### Download & Installation

#### Automatic Installation (Recommended)
```bash
pip install paddlepaddle paddleocr
```
Models are downloaded automatically on first use.

#### Manual Download
```bash
# Detection model
wget https://paddleocr.bj.bcebos.com/PP-OCRv4/english/en_PP-OCRv4_det_infer.tar
tar -xf en_PP-OCRv4_det_infer.tar

# Recognition model  
wget https://paddleocr.bj.bcebos.com/PP-OCRv4/english/en_PP-OCRv4_rec_infer.tar
tar -xf en_PP-OCRv4_rec_infer.tar

# Classification model
wget https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_cls_infer.tar
tar -xf ch_ppocr_mobile_v2.0_cls_infer.tar
```

### Directory Structure
```
models/paddleocr/
├── det_model/
│   ├── inference.pdiparams
│   ├── inference.pdiparams.info
│   └── inference.pdmodel
├── rec_model/
│   ├── inference.pdiparams
│   ├── inference.pdiparams.info
│   └── inference.pdmodel
└── cls_model/
    ├── inference.pdiparams
    ├── inference.pdiparams.info
    └── inference.pdmodel
```

### Configuration
```python
# In ocr/ocr_engine.py
from paddleocr import PaddleOCR

ocr = PaddleOCR(
    use_angle_cls=True,
    lang='en',  # or 'ch' for Chinese/multilingual
    det_model_dir='models/paddleocr/det_model',
    rec_model_dir='models/paddleocr/rec_model',
    cls_model_dir='models/paddleocr/cls_model'
)
```

---

## 2. Translation Model (NLLB-200)

### Model Information
- **Framework**: Transformers (Hugging Face)
- **Model**: Meta's No Language Left Behind (NLLB-200)
- **Purpose**: Neural machine translation for 200+ languages
- **Size**: 600MB (distilled) to 15GB (full model)
- **Languages**: Nepali (npi_Deva), Sinhala (sin_Sinh), English (eng_Latn)

### Download Options

#### Option 1: Distilled Model (Recommended for CPU)
```bash
# Download via Hugging Face Hub
pip install transformers torch

# Python script to download
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "facebook/nllb-200-distilled-600M"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Save locally
tokenizer.save_pretrained("models/nllb/")
model.save_pretrained("models/nllb/")
```

#### Option 2: Full Model (Better Quality)
```bash
# For better translation quality (requires more resources)
model_name = "facebook/nllb-200-1.3B"  # or "facebook/nllb-200-3.3B"
```

#### Option 3: Quantized GGUF (Fastest)
```bash
# Download quantized version for faster inference
wget https://huggingface.co/microsoft/nllb-200-distilled-600M-GGUF/resolve/main/nllb-200-distilled-600M-q4_0.gguf
```

### Direct Download Links
- **Distilled 600M**: https://huggingface.co/facebook/nllb-200-distilled-600M
- **1.3B Model**: https://huggingface.co/facebook/nllb-200-1.3B  
- **3.3B Model**: https://huggingface.co/facebook/nllb-200-3.3B
- **GGUF Quantized**: https://huggingface.co/microsoft/nllb-200-distilled-600M-GGUF

### Directory Structure
```
models/nllb/
├── config.json
├── pytorch_model.bin
├── tokenizer.json
├── tokenizer_config.json
├── special_tokens_map.json
└── vocab.json
```

### Language Codes
```python
LANGUAGE_CODES = {
    'nepali': 'npi_Deva',
    'sinhala': 'sin_Sinh', 
    'english': 'eng_Latn',
    'hindi': 'hin_Deva',
    'bengali': 'ben_Beng'
}
```

---

## 3. Language Detection Model (FastText)

### Model Information
- **Framework**: FastText (Meta)
- **Purpose**: Automatic language identification
- **Size**: ~126 MB
- **Languages**: 176 languages supported
- **Accuracy**: 93.7% on validation set

### Download & Installation

#### Option 1: Official FastText Model
```bash
# Install FastText
pip install fasttext

# Download language identification model
wget https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin

# Move to models directory
mv lid.176.bin models/fasttext/
```

#### Option 2: Compressed Model
```bash
# Smaller compressed version
wget https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz
mv lid.176.ftz models/fasttext/
```

### Direct Download Links
- **Full Model**: https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
- **Compressed**: https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz

### Directory Structure
```
models/fasttext/
└── lid.176.bin  # or lid.176.ftz
```

### Usage Example
```python
import fasttext

model = fasttext.load_model('models/fasttext/lid.176.bin')
predictions = model.predict("नमस्ते", k=3)
# Returns: (('__label__ne',), array([0.99999]))
```

---

## 4. LLM Model (Phi-3 Mini)

### Model Information
- **Framework**: Transformers / GGUF
- **Model**: Microsoft Phi-3 Mini
- **Purpose**: Text post-processing, summarization, quality improvement
- **Size**: 2.4GB (4-bit quantized) to 7GB (full precision)
- **Context Length**: 128K tokens

### Download Options

#### Option 1: Hugging Face Transformers
```bash
pip install transformers torch

# Python download script
from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "microsoft/Phi-3-mini-4k-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

tokenizer.save_pretrained("models/phi3/")
model.save_pretrained("models/phi3/")
```

#### Option 2: GGUF Quantized (Recommended)
```bash
# Download quantized GGUF model for faster inference
wget https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf

# Move to models directory
mv Phi-3-mini-4k-instruct-q4.gguf models/phi3/
```

### Direct Download Links
- **Phi-3 Mini**: https://huggingface.co/microsoft/Phi-3-mini-4k-instruct
- **GGUF Quantized**: https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf
- **Alternative**: https://huggingface.co/bartowski/Phi-3-mini-4k-instruct-GGUF

### Directory Structure
```
models/phi3/
├── config.json
├── pytorch_model.bin
├── tokenizer.json
├── tokenizer_config.json
└── special_tokens_map.json
```

---

## Complete Setup Script

### Windows (setup_models.bat)
```batch
@echo off
echo Downloading all required models...

REM Create directories
mkdir models\paddleocr
mkdir models\nllb  
mkdir models\fasttext
mkdir models\phi3

REM Install Python packages
pip install paddleocr transformers torch fasttext

REM Download FastText model
echo Downloading FastText language detection model...
curl -L https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin -o models\fasttext\lid.176.bin

REM Download NLLB model (Python script needed)
echo Downloading NLLB translation model...
python -c "
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
model_name = 'facebook/nllb-200-distilled-600M'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer.save_pretrained('models/nllb/')
model.save_pretrained('models/nllb/')
print('NLLB model downloaded successfully')
"

REM Download Phi-3 model
echo Downloading Phi-3 model...
python -c "
from transformers import AutoTokenizer, AutoModelForCausalLM
model_name = 'microsoft/Phi-3-mini-4k-instruct'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer.save_pretrained('models/phi3/')
model.save_pretrained('models/phi3/')
print('Phi-3 model downloaded successfully')
"

echo All models downloaded successfully!
pause
```

### Linux/macOS (setup_models.sh)
```bash
#!/bin/bash
echo "Downloading all required models..."

# Create directories
mkdir -p models/{paddleocr,nllb,fasttext,phi3}

# Install Python packages
pip install paddleocr transformers torch fasttext

# Download FastText model
echo "Downloading FastText language detection model..."
wget https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin -O models/fasttext/lid.176.bin

# Download NLLB model
echo "Downloading NLLB translation model..."
python3 -c "
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
model_name = 'facebook/nllb-200-distilled-600M'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer.save_pretrained('models/nllb/')
model.save_pretrained('models/nllb/')
print('NLLB model downloaded successfully')
"

# Download Phi-3 model
echo "Downloading Phi-3 model..."
python3 -c "
from transformers import AutoTokenizer, AutoModelForCausalLM
model_name = 'microsoft/Phi-3-mini-4k-instruct'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer.save_pretrained('models/phi3/')
model.save_pretrained('models/phi3/')
print('Phi-3 model downloaded successfully')
"

echo "All models downloaded successfully!"
```

---

## Model Verification

### Check Downloaded Models
```python
import os
from pathlib import Path

def verify_models():
    models_dir = Path("models")
    
    # Check PaddleOCR (auto-downloaded)
    print("✅ PaddleOCR: Auto-downloaded on first use")
    
    # Check NLLB
    nllb_path = models_dir / "nllb" / "config.json"
    print(f"{'✅' if nllb_path.exists() else '❌'} NLLB: {nllb_path}")
    
    # Check FastText
    fasttext_path = models_dir / "fasttext" / "lid.176.bin"
    print(f"{'✅' if fasttext_path.exists() else '❌'} FastText: {fasttext_path}")
    
    # Check Phi-3
    phi3_path = models_dir / "phi3" / "config.json"
    print(f"{'✅' if phi3_path.exists() else '❌'} Phi-3: {phi3_path}")

if __name__ == "__main__":
    verify_models()
```

---

## Performance Optimization

### Model Quantization
```python
# For faster inference, use quantized models
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Load with 8-bit quantization
model = AutoModelForSeq2SeqLM.from_pretrained(
    "facebook/nllb-200-distilled-600M",
    load_in_8bit=True,
    device_map="auto"
)
```

### GPU Acceleration
```python
# Enable GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
```

---

## Troubleshooting

### Common Issues

1. **Out of Memory**
   - Use smaller/quantized models
   - Reduce batch size
   - Enable CPU offloading

2. **Slow Download**
   - Use mirror sites
   - Download during off-peak hours
   - Use wget/curl with resume capability

3. **Model Loading Errors**
   - Verify file integrity
   - Check available disk space
   - Ensure correct file permissions

### Alternative Download Methods

#### Using Git LFS
```bash
git lfs install
git clone https://huggingface.co/facebook/nllb-200-distilled-600M models/nllb
```

#### Using Hugging Face CLI
```bash
pip install huggingface_hub
huggingface-cli download facebook/nllb-200-distilled-600M --local-dir models/nllb
```

---

## Model Licenses

- **PaddleOCR**: Apache 2.0
- **NLLB-200**: CC-BY-NC 4.0 (Non-commercial use)
- **FastText**: MIT License
- **Phi-3**: MIT License

**Note**: Ensure compliance with model licenses for your use case, especially for commercial applications.

---

## Total Storage Requirements

| Model | Size | Purpose |
|-------|------|---------|
| PaddleOCR | ~400 MB | OCR |
| NLLB-200 (Distilled) | ~600 MB | Translation |
| FastText | ~126 MB | Language Detection |
| Phi-3 Mini | ~2.4 GB | Post-processing |
| **Total** | **~3.5 GB** | Complete Pipeline |

**Recommended**: 10+ GB free space for models and temporary files.