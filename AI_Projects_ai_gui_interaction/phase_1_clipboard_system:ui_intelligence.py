import pytesseract
from PIL import ImageGrab, ImageEnhance
import pyautogui
import time
import os
import re
from difflib import SequenceMatcher

def normalize_text(text):
    """Clean OCR text for fuzzy matching"""
    return re.sub(r'\s+', ' ', text.lower().strip())

class UIIntelligence:
    def __init__(self):
        self.screenshot_dir = os.path.join(os.path.dirname(__file__), "screenshots")
        os.makedirs(self.screenshot_dir, exist_ok=True)

    def capture_boosted_image(self):
        """Grab screen and apply contrast boost"""
        img = ImageGrab.grab()
        enhancer = ImageEnhance.Contrast(img)
        return enhancer.enhance(3.5)

    def fuzzy_locate_text(self, target_text, threshold=0.8):
        """Find screen coords of text using fuzzy matching"""
        img = self.capture_boosted_image()

        # Save for inspection
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        path = os.path.join(self.screenshot_dir, f"ocr_boosted_{timestamp}.png")
        img.save(path)

        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        target_norm = normalize_text(target_text)

        print("🔍 OCR words detected:")
        for i, word in enumerate(data['text']):
            raw = word.strip()
            if raw:
                guess = normalize_text(raw)
                similarity = SequenceMatcher(None, target_norm, guess).ratio()
                print(f"  → '{raw}' (similarity: {similarity:.2f})")
                if similarity >= threshold:
                    x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                    print(f"✅ Fuzzy match: '{raw}' @ ({x},{y})")
                    return (x + w // 2, y + h // 2)
        print("❌ No suitable fuzzy match found.")
        return None

    def click_and_copy(self, coords):
        x, y = coords
        pyautogui.click(x, y)
        time.sleep(0.3)
        pyautogui.hotkey("command", "a")
        time.sleep(0.1)
        pyautogui.hotkey("command", "c")
        time.sleep(0.1)
        return self.get_clipboard_text()

    def get_clipboard_text(self):
        try:
            from subprocess import check_output
            return check_output("pbpaste", universal_newlines=True).strip()
        except Exception as e:
            return f"Clipboard error: {e}"

    def verify_clipboard_content(self, content):
        return "Valid" if content and len(content.strip()) > 0 else "Empty or invalid"

    def fallback_input_capture(self):
        print("🟡 Fallback triggered — no real capture.")
        return "Fallback dummy input."
