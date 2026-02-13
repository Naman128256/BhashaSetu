#!/usr/bin/env python3
"""
Test real translation functionality
"""

import requests
import json

def test_translation():
    """Test translation with real backend"""
    
    backend_url = "http://127.0.0.1:5005"
    
    # Test cases
    tests = [
        {
            "text": "සාහිත්යය යනු මානව සභ්යතාවේ දර්පණයකි",
            "source": "sinhala",
            "target": "english",
            "description": "Sinhala literature text"
        },
        {
            "text": "नमस्ते, तपाईंलाई कस्तो छ?",
            "source": "nepali", 
            "target": "english",
            "description": "Simple Nepali greeting"
        }
    ]
    
    print("Testing Real Translation System")
    print("=" * 50)
    
    for i, test in enumerate(tests, 1):
        print(f"\nTest {i}: {test['description']}")
        print(f"Original: {test['text']}")
        
        try:
            response = requests.post(f"{backend_url}/translate", 
                                   json={
                                       "text": test['text'],
                                       "source_lang": test['source'],
                                       "target_lang": test['target']
                                   }, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                print(f"Translation: {result.get('translated_text')}")
                print(f"Confidence: {result.get('confidence', 0):.1%}")
                
                # Check if it's real or mock
                confidence = result.get('confidence', 0)
                if confidence > 0.8:
                    print("Status: Using REAL NLLB model")
                else:
                    print("Status: Using enhanced mock responses")
            else:
                print(f"Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"Exception: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    test_translation()