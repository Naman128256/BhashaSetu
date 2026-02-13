#!/usr/bin/env python3
"""
Test Sinhala translation functionality
"""

import requests
import json

def test_sinhala_translation():
    """Test various Sinhala texts"""
    
    test_texts = [
        {
            "text": "සාහිත්යය යනු මානව සභ්යතාවේ දර්පණයකි. එය අපගේ සංස්කෘතිය සහ සම්ප්රදායන් පිළිබිඹු කරයි.",
            "description": "Literature and culture"
        },
        {
            "text": "ශ්රී ලංකාවේ බුද්ධ ධර්මය දහස් ගණන් වසරක් තිස්සේ සමාජයට මග පෙන්වා ඇත.",
            "description": "Buddhism in Sri Lanka"
        },
        {
            "text": "භාෂාව යනු මානව සන්නිවේදනයේ මූලික අංගයකි. එය සංස්කෘතික අනන්යතාවය ආරක්ෂා කරයි.",
            "description": "Language and communication"
        },
        {
            "text": "කලාව මානව අත්දැකීම්වල නිර්මාණාත්මක ප්රකාශනයකි.",
            "description": "Art and creativity"
        },
        {
            "text": "අධ්යාපනය ප්රගතියේ සහ ප්රබුද්ධත්වයේ පදනමයි.",
            "description": "Education and progress"
        }
    ]
    
    backend_url = "http://127.0.0.1:5005"
    
    print("Testing Sinhala Translation System")
    print("=" * 50)
    
    for i, test in enumerate(test_texts, 1):
        print(f"\nTest {i}: {test['description']}")
        print(f"Original: {test['text']}")
        
        try:
            # Test language detection
            lang_response = requests.post(f"{backend_url}/detect-language", 
                                        json={"text": test['text']}, timeout=10)
            
            if lang_response.status_code == 200:
                lang_result = lang_response.json()
                print(f"Detected: {lang_result.get('language')} ({lang_result.get('confidence', 0):.1%})")
            
            # Test translation
            trans_response = requests.post(f"{backend_url}/translate", 
                                         json={
                                             "text": test['text'],
                                             "source_lang": "sinhala",
                                             "target_lang": "english"
                                         }, timeout=15)
            
            if trans_response.status_code == 200:
                trans_result = trans_response.json()
                print(f"Translation: {trans_result.get('translated_text')}")
                print(f"Confidence: {trans_result.get('confidence', 0):.1%}")
            else:
                print(f"Translation failed: {trans_response.status_code}")
                
        except Exception as e:
            print(f"Error: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    test_sinhala_translation()