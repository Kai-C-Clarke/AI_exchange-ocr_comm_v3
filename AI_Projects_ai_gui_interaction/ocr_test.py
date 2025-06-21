from PIL import ImageGrab
import pytesseract

# Capture screen and save for inspection
img = ImageGrab.grab()
img.save("screen_capture.png")

# Print what Tesseract sees
text = pytesseract.image_to_string(img)
print("OCR Output:\n", text)
