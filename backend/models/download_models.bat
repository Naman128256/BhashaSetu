@echo off
setlocal enabledelayedexpansion

echo ==========================================================
echo        SMART CHECK: DOWNLOAD ONLY IF NOT PRESENT
echo ==========================================================

echo.
echo Checking FastText model...

if exist "models\lid.176.ftz" (
    echo FastText already exists - skipping.
) else (
    echo Downloading FastText model...
    mkdir models 2>nul
    curl -L -o "models\lid.176.ftz" https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz
)

echo.
echo Checking NLLB model...

if exist "models\nllb_model" (
    echo NLLB model already exists - skipping.
) else (
    echo Downloading NLLB model...
    mkdir models\nllb_model 2>nul
    curl -L -o "models\nllb_model\pytorch_model.bin" https://huggingface.co/facebook/nllb-200-distilled-600M/resolve/main/pytorch_model.bin
)

echo.
echo All downloads complete.
pause
