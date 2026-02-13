@echo off
echo ========================================
echo    FIXING MISSING COMPONENTS
echo ========================================

echo.
echo [1/3] Installing Python dependencies...
pip install transformers torch fasttext paddleocr sentencepiece

echo.
echo [2/3] Creating directories...
if not exist "models\models\nllb_model" mkdir models\models\nllb_model

echo.
echo [3/3] Downloading NLLB tokenizer files...
cd models\models\nllb_model

echo Downloading config.json...
curl -L -o config.json https://huggingface.co/facebook/nllb-200-distilled-600M/resolve/main/config.json

echo Downloading tokenizer.json...
curl -L -o tokenizer.json https://huggingface.co/facebook/nllb-200-distilled-600M/resolve/main/tokenizer.json

echo Downloading tokenizer_config.json...
curl -L -o tokenizer_config.json https://huggingface.co/facebook/nllb-200-distilled-600M/resolve/main/tokenizer_config.json

echo Downloading sentencepiece model...
curl -L -o sentencepiece.bpe.model https://huggingface.co/facebook/nllb-200-distilled-600M/resolve/main/sentencepiece.bpe.model

echo Downloading special tokens map...
curl -L -o special_tokens_map.json https://huggingface.co/facebook/nllb-200-distilled-600M/resolve/main/special_tokens_map.json

cd ..\..\..

echo.
echo [4/4] Starting backend server...
python app.py

echo.
echo ========================================
echo    SETUP COMPLETE!
echo ========================================
echo.
echo Run 'python app.py' to start the backend
pause