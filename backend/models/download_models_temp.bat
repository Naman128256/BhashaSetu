@echo off
setlocal enabledelayedexpansion

echo ==========================================================
echo           SMART MODEL DOWNLOADER - BACKEND
echo           DOWNLOAD ONLY IF NOT PRESENT
echo ==========================================================

REM ----------------------------------------------------------
REM Create models directory if not exists
REM ----------------------------------------------------------

if not exist "models" (
    mkdir "models"
)

echo.
echo -------------------------------------------
echo Checking FastText Model
echo -------------------------------------------

if exist "models\lid.176.ftz" (
    echo FastText model already exists. Skipping.
) else (
    echo Downloading FastText model...
    curl -L -o "models\lid.176.ftz" ^
https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz
)

echo.
echo -------------------------------------------
echo Checking NLLB Model
echo -------------------------------------------

if exist "models\nllb_600m" (
    echo NLLB folder already exists. Skipping.
) else (
    echo Creating NLLB folder...
    mkdir "models\nllb_600m"

    echo Downloading NLLB model weights...
    curl -L -o "models\nllb_600m\pytorch_model.bin" ^
https://huggingface.co/facebook/nllb-200-distilled-600M/resolve/main/pytorch_model.bin

    echo Downloading NLLB config.json...
    curl -L -o "models\nllb_600m\config.json" ^
https://huggingface.co/facebook/nllb-200-distilled-600M/resolve/main/config.json

    echo Downloading NLLB tokenizer.json...
    curl -L -o "models\nllb_600m\tokenizer.json" ^
https://huggingface.co/facebook/nllb-200-distilled-600M/resolve/main/tokenizer.json

    echo Downloading NLLB sentencepiece model...
    curl -L -o "models\nllb_600m\sentencepiece.bpe.model" ^
https://huggingface.co/facebook/nllb-200-distilled-600M/resolve/main/sentencepiece.bpe.model
)

echo.
echo -------------------------------------------
echo Checking PaddleOCR Models
echo -------------------------------------------

if exist "models\paddleocr" (
    echo PaddleOCR models already exist. Skipping.
) else (
    echo Creating PaddleOCR folder...
    mkdir "models\paddleocr"

    echo Downloading PP-OCRv4 English detection model...
    curl -L -o "models\paddleocr\det_model.pdparams" ^
https://paddleocr.bj.bcebos.com/PP-OCRv4/ch_PP-OCRv4_det_infer.tar

    echo Downloading PP-OCRv4 English recognition model...
    curl -L -o "models\paddleocr\rec_model.pdparams" ^
https://paddleocr.bj.bcebos.com/PP-OCRv4/ch_PP-OCRv4_rec_infer.tar
)

echo.
echo -------------------------------------------
echo Checking DocTR Models
echo -------------------------------------------

if exist "models\doctr" (
    echo DocTR models already exist. Skipping.
) else (
    echo Creating DocTR folder...
    mkdir "models\doctr"

    echo DocTR uses runtime downloads, creating placeholder...
    echo doctr placeholder > models\doctr\README.txt
)

echo.
echo -------------------------------------------
echo Model Downloads Finished
echo -------------------------------------------
pause
