# Frontend - Nepali & Sinhala Literature Translator

Streamlit-based web interface for the offline literature translator.

## Features

### 📝 Text Input Mode
- Direct text input for Nepali/Sinhala text
- Real-time language detection with confidence scores
- Translation to English/Nepali/Sinhala
- Script detection (Devanagari, Sinhala, Latin)

### 📷 Image Upload Mode (OCR)
- Upload images (PNG, JPG, PDF, TIFF, BMP)
- OCR text extraction
- Automatic language detection
- Translation with accuracy scores
- Text summarization
- Processing time tracking

## Quick Start

### Prerequisites
- Backend server must be running on `http://127.0.0.1:5005`
- Python 3.10+ with pip

### Installation & Run

#### Windows
```cmd
cd frontend
run_frontend.bat
```

#### Linux/macOS
```bash
cd frontend
chmod +x run_frontend.sh
./run_frontend.sh
```

#### Manual Setup
```bash
# Install dependencies
pip install streamlit requests Pillow

# Start frontend
streamlit run app.py
```

## Usage

1. **Start Backend**: Ensure backend is running first
2. **Open Frontend**: Access at `http://localhost:8501`
3. **Choose Mode**: Text input or image upload
4. **Select Target Language**: English, Nepali, or Sinhala
5. **Process**: Get OCR, language detection, and translation results

## API Integration

The frontend communicates with the Flask backend via REST API:

- `GET /health` - Backend status check
- `POST /detect-language` - Language detection
- `POST /translate` - Text translation
- `POST /upload` - File upload for OCR
- `GET /status/<job_id>` - Processing status
- `GET /result/<job_id>` - Final results

## Output Information

### Language Detection
- Detected language name
- Confidence percentage
- Script type (Devanagari/Sinhala/Latin)

### Translation
- Translated text
- Source → Target language mapping
- Translation confidence score

### OCR Results
- Extracted text from images
- Processing status and progress
- Error handling and fallbacks

## Troubleshooting

### Backend Not Running
```bash
# Start backend first
cd ../backend
./run.sh  # or run.bat on Windows
```

### Port Issues
- Frontend: `http://localhost:8501`
- Backend: `http://127.0.0.1:5005`

### Dependencies
```bash
pip install streamlit requests Pillow
```

## Sample Texts for Testing

### Nepali
```
नमस्ते, तपाईंलाई कस्तो छ?
साहित्यमा भाषाको महत्व अत्यधिक छ।
```

### Sinhala
```
සුභ දවසක් වේවා!
සාහිත්යය යනු මානව සභ්යතාවේ දර්පණයකි।
ශ්රී ලංකාවේ බුද්ධ ධර්මය දහස් ගණන් වසරක් තිස්සේ සමාජයට මග පෙන්වා ඇත।
භාෂාව යනු මානව සන්නිවේදනයේ මූලික අංගයකි।
```