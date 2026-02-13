# Installation Guide - Nepali & Sinhala Literature Translator Backend

## Quick Installation

### Windows
```cmd
cd backend
start.bat
```

### Linux/macOS
```bash
cd backend
chmod +x start.sh
./start.sh
```

## Manual Installation

### 1. Prerequisites
- Python 3.13 (recommended) or Python 3.10+
- pip 23+
- 8+ GB RAM
- 10+ GB free disk space

### 2. Setup Virtual Environment
```bash
# Create virtual environment
python3.13 -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/macOS)
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create Directories
```bash
mkdir logs temp models
```

### 5. Test Setup
```bash
python test_setup.py
```

### 6. Start Backend
```bash
python app.py
```

## Verification

Backend should be accessible at: `http://127.0.0.1:5005`

Test with:
```bash
curl http://127.0.0.1:5005/health
```

Expected response:
```json
{
  "status": "ok",
  "timestamp": 1642781234.567,
  "service": "nepali-sinhala-translator-backend"
}
```

## Building Executable

### Windows
```cmd
build.bat
```

### Linux/macOS
```bash
chmod +x build.sh
./build.sh
```

Executable will be created in `dist/` directory.

## Troubleshooting

### Common Issues

1. **Port 5005 already in use**
   ```bash
   # Windows
   netstat -ano | findstr :5005
   
   # Linux/macOS
   lsof -i :5005
   ```

2. **Import errors**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall
   ```

3. **Permission errors**
   ```bash
   # Windows: Run as Administrator
   # Linux/macOS: Check file permissions
   chmod +x start.sh build.sh
   ```

4. **Memory issues**
   - Ensure 8+ GB RAM available
   - Close other applications
   - Use quantized models

### Debug Mode
```bash
# Enable debug logging
export FLASK_DEBUG=true
export LOG_LEVEL=DEBUG
python app.py
```

## Next Steps

1. Download ML models (see README.md)
2. Configure Electron frontend
3. Test end-to-end workflow
4. Deploy as standalone executable

For detailed documentation, see:
- `README.md` - Complete usage guide
- `ARCHITECTURE.md` - Technical architecture
- `backend/` - Source code