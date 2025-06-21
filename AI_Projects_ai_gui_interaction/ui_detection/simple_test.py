#!/usr/bin/env python3

print("🔍 Starting simple OCR test...")

try:
    from PIL import ImageGrab
    print("✅ PIL ImageGrab imported")
    
    import pytesseract
    print("✅ pytesseract imported")
    
    # Test screenshot
    print("📸 Taking screenshot...")
    img = ImageGrab.grab()
    print(f"✅ Screenshot captured: {img.size}")
    
    # Save it
    img.save("test_screenshot.png")
    print("✅ Screenshot saved as test_screenshot.png")
    
    # Test OCR on a small region
    print("🔍 Testing OCR...")
    # Just test top-left corner to start
    small_region = img.crop((0, 0, 300, 100))
    text = pytesseract.image_to_string(small_region)
    print(f"✅ OCR result: '{text.strip()}'")
    
    print("🎉 All basic functions working!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()