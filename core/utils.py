# core/utils.py

import pyautogui
import pytesseract
from PIL import ImageGrab

def scroll_area_and_capture_text(region):
    """
    Scrolls and captures OCR text from a region of the screen.
    """
    screenshot = ImageGrab.grab(bbox=region)
    text = pytesseract.image_to_string(screenshot)
    return text
