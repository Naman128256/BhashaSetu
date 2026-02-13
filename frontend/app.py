import streamlit as st
import requests
import json
from PIL import Image
import io
import time

# Backend API configuration
BACKEND_URL = "http://127.0.0.1:5005"

def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def detect_language(text):
    """Detect language of text"""
    try:
        response = requests.post(f"{BACKEND_URL}/detect-language", 
                               json={"text": text}, timeout=10)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def translate_text(text, source_lang="auto", target_lang="en"):
    """Translate text"""
    try:
        response = requests.post(f"{BACKEND_URL}/translate", 
                               json={"text": text, "source_lang": source_lang, "target_lang": target_lang}, 
                               timeout=30)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def upload_file_for_ocr(file):
    """Upload file for OCR processing"""
    try:
        files = {"file": file}
        response = requests.post(f"{BACKEND_URL}/upload", files=files, timeout=30)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_job_status(job_id):
    """Get processing job status"""
    try:
        response = requests.get(f"{BACKEND_URL}/status/{job_id}", timeout=10)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_job_result(job_id):
    """Get processing job result"""
    try:
        response = requests.get(f"{BACKEND_URL}/result/{job_id}", timeout=10)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def main():
    st.set_page_config(
        page_title="Nepali & Sinhala Literature Translator",
        page_icon="🌏",
        layout="wide"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-text {
        color: #28a745;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">🌏 Nepali & Sinhala Literature Translator</h1>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Advanced OCR, Language Detection & Translation System</p>", unsafe_allow_html=True)
    
    # Check backend status
    if not check_backend():
        st.error("❌ Backend server is not running. Please start the backend first.")
        st.code("cd backend && python app.py")
        return
    
    st.success("✅ Backend server is running")
    
    # Sidebar for options
    st.sidebar.title("Options")
    mode = st.sidebar.selectbox("Select Mode", ["Text Input", "Image Upload (OCR)"])
    target_lang = st.sidebar.selectbox("Target Language", ["English", "Nepali", "Sinhala"])
    
    lang_map = {"English": "en", "Nepali": "ne", "Sinhala": "si"}
    target_code = lang_map[target_lang]
    
    if mode == "Text Input":
        st.header("📝 Text Translation")
        
        # Text input
        input_text = st.text_area("Enter Nepali or Sinhala text:", height=150, 
                                 placeholder="नमस्ते, तपाईंलाई कस्तो छ? or සුභ දවසක් වේවා!")
        
        if st.button("🔍 Analyze & Translate", type="primary"):
            if input_text.strip():
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("🔍 Language Detection")
                    with st.spinner("Detecting language..."):
                        lang_result = detect_language(input_text)
                    
                    if "error" not in lang_result:
                        # Display metrics in a nice format
                        col1_1, col1_2, col1_3 = st.columns(3)
                        with col1_1:
                            st.metric("Language", lang_result.get('language', 'Unknown').title())
                        with col1_2:
                            st.metric("Confidence", f"{lang_result.get('confidence', 0):.1%}")
                        with col1_3:
                            st.metric("Script", lang_result.get('script', 'Unknown').title())
                        
                        # Store detected language for translation
                        detected_lang = lang_result.get('language', 'auto')
                    else:
                        st.error(f"Language detection failed: {lang_result['error']}")
                        detected_lang = "auto"
                
                with col2:
                    st.subheader("🌐 Translation")
                    with st.spinner("Translating..."):
                        trans_result = translate_text(input_text, detected_lang, target_code)
                    
                    if "error" not in trans_result:
                        st.success("**Translation Result:**")
                        # Display translation in a text area for better readability
                        st.text_area("Translated Text:", value=trans_result.get('translated_text', 'No translation'), height=100, disabled=True)
                        
                        # Translation metrics
                        col2_1, col2_2 = st.columns(2)
                        with col2_1:
                            st.metric("From → To", f"{trans_result.get('source_language', 'Unknown')} → {trans_result.get('target_language', 'Unknown')}")
                        with col2_2:
                            if 'confidence' in trans_result:
                                st.metric("Translation Accuracy", f"{trans_result['confidence']:.1%}")
                    else:
                        st.error(f"Translation failed: {trans_result['error']}")
            else:
                st.warning("Please enter some text to analyze")
    
    else:  # Image Upload mode
        st.header("📷 Image OCR & Translation")
        
        uploaded_file = st.file_uploader("Upload an image with Nepali/Sinhala text", 
                                       type=['png', 'jpg', 'jpeg', 'pdf', 'tiff', 'bmp'])
        
        if uploaded_file is not None:
            # Display uploaded image
            if uploaded_file.type.startswith('image'):
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", use_column_width=True)
            
            if st.button("🔍 Process Image", type="primary"):
                # Upload file for processing
                with st.spinner("Uploading file..."):
                    upload_result = upload_file_for_ocr(uploaded_file)
                
                if "error" not in upload_result:
                    job_id = upload_result.get('job_id')
                    st.success(f"File uploaded successfully! Job ID: {job_id}")
                    
                    # Poll for job completion
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    while True:
                        status_result = get_job_status(job_id)
                        
                        if "error" not in status_result:
                            status = status_result.get('status')
                            progress = status_result.get('progress', 0)
                            message = status_result.get('message', '')
                            
                            progress_bar.progress(progress / 100)
                            status_text.text(f"Status: {status} - {message}")
                            
                            if status == 'completed':
                                break
                            elif status == 'failed':
                                st.error(f"Processing failed: {status_result.get('error', 'Unknown error')}")
                                return
                        
                        time.sleep(2)
                    
                    # Get final results
                    with st.spinner("Retrieving results..."):
                        result = get_job_result(job_id)
                    
                    if "error" not in result:
                        st.success("✅ Processing completed!")
                        
                        # Display results in columns
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.subheader("📝 OCR Results")
                            original_text = result.get('original_text', 'No text extracted')
                            st.text_area("Extracted Text:", value=original_text, height=200)
                        
                        with col2:
                            st.subheader("🔍 Language Detection")
                            lang_info = result.get('detected_language', {})
                            if lang_info:
                                st.success(f"**Language:** {lang_info.get('language', 'Unknown').title()}")
                                st.info(f"**Confidence:** {lang_info.get('confidence', 0):.2%}")
                                st.info(f"**Script:** {lang_info.get('script', 'Unknown').title()}")
                        
                        with col3:
                            st.subheader("🌐 Translation")
                            translation_info = result.get('translation', {})
                            if translation_info:
                                translated_text = translation_info.get('translated_text', 'No translation')
                                st.text_area("Translation:", value=translated_text, height=200)
                                st.info(f"**Confidence:** {translation_info.get('confidence', 0):.2%}")
                        
                        # Summary section
                        st.subheader("📊 Processing Summary")
                        summary_info = result.get('summary', {})
                        if summary_info:
                            st.write("**Summary:**")
                            st.write(summary_info.get('summary', 'No summary available'))
                        
                        processing_time = result.get('processing_time', 0)
                        st.info(f"**Total Processing Time:** {processing_time:.2f} seconds")
                    
                    else:
                        st.error(f"Failed to get results: {result['error']}")
                
                else:
                    st.error(f"File upload failed: {upload_result['error']}")

if __name__ == "__main__":
    main()