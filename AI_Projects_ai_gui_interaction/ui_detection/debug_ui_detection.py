#!/usr/bin/env python3

import pytesseract
from PIL import ImageGrab, ImageEnhance
import time
import os

def quick_chatgpt_debug():
    """Efficient OCR debug for ChatGPT input detection"""
    
    print("🔍 Quick ChatGPT UI Debug")
    print("Switch to ChatGPT now - starting in 3 seconds...")
    time.sleep(3)
    
    # Capture screenshot
    print("📸 Taking screenshot...")
    img = ImageGrab.grab()
    print(f"Screenshot size: {img.size}")
    
    # Resize for faster processing (your screen is 4K!)
    # Scale down to 2048 width for speed
    scale_factor = 2048 / img.width
    new_size = (int(img.width * scale_factor), int(img.height * scale_factor))
    img_resized = img.resize(new_size)
    print(f"Resized to: {img_resized.size}")
    
    # Focus on bottom half where input field likely is
    width, height = img_resized.size
    bottom_half = img_resized.crop((0, height//2, width, height))
    
    # Apply contrast boost
    enhancer = ImageEnhance.Contrast(bottom_half)
    boosted = enhancer.enhance(2.0)
    
    # Save for inspection
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    boosted.save(f"chatgpt_bottom_half_{timestamp}.png")
    print(f"Saved bottom half: chatgpt_bottom_half_{timestamp}.png")
    
    # Run OCR on bottom half only
    print("🔍 Running OCR on bottom half...")
    try:
        data = pytesseract.image_to_data(boosted, output_type=pytesseract.Output.DICT)
        
        # Look for input-related text
        input_keywords = ['ask', 'anything', 'type', 'message', 'send', 'chat']
        found_elements = []
        
        print("\n=== TEXT DETECTED IN BOTTOM HALF ===")
        for i, text in enumerate(data['text']):
            if text.strip() and int(data['conf'][i]) > 30:
                print(f"'{text}' (confidence: {data['conf'][i]})")
                
                # Check if it's input-related
                text_lower = text.lower()
                for keyword in input_keywords:
                    if keyword in text_lower:
                        x = data['left'][i]
                        y = data['top'][i] + height//2  # Adjust for crop
                        w = data['width'][i] 
                        h = data['height'][i]
                        
                        # Scale back to original coordinates
                        orig_x = int(x / scale_factor)
                        orig_y = int(y / scale_factor)
                        
                        found_elements.append({
                            'text': text,
                            'keyword': keyword,
                            'coords': (orig_x + w//2, orig_y + h//2),
                            'confidence': data['conf'][i]
                        })
                        
                        print(f"🎯 POTENTIAL INPUT: '{text}' at original coords ({orig_x}, {orig_y})")
        
        if not found_elements:
            print("\n❌ No input-related keywords found")
            print("This suggests ChatGPT input field uses placeholder text or no text")
            print("We should switch to visual detection method!")
        else:
            print(f"\n✅ Found {len(found_elements)} potential input elements")
            return found_elements[0]['coords']  # Return best match
            
    except Exception as e:
        print(f"❌ OCR Error: {e}")
        return None

def fallback_position_guess():
    """Smart position guess for ChatGPT input"""
    img = ImageGrab.grab()
    width, height = img.size
    
    # ChatGPT input is typically:
    # - Horizontally centered 
    # - In bottom 15% of screen
    # - Slightly left of absolute center
    
    guess_x = int(width * 0.48)  # Slightly left of center
    guess_y = int(height * 0.85)  # Bottom area
    
    print(f"🎯 Fallback guess: ({guess_x}, {guess_y})")
    return (guess_x, guess_y)

if __name__ == "__main__":
    result = quick_chatgpt_debug()
    
    if not result:
        print("\n🟡 OCR detection failed - using position fallback")
        result = fallback_position_guess()
    
    print(f"\n🎯 Target coordinates: {result}")
    print("\n💡 Next step: Test clicking these coordinates!")
    print("Add this to your ui_intelligence.py:")
    print(f"coords = {result}")
    print("content = ui.click_and_copy(coords)")