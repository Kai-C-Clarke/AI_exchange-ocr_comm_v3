from PIL import ImageGrab, ImageEnhance
import pytesseract

# Grab the screen
img = ImageGrab.grab()

# Boost contrast
enhancer = ImageEnhance.Contrast(img)
img_boosted = enhancer.enhance(3.0)  # Try 2.5–4.0 if needed

# Optional: save for inspection
img_boosted.save("boosted_capture.png")

# OCR read
text = pytesseract.image_to_string(img_boosted)
print("OCR Output:\n", text)
