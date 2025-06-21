from PIL import ImageGrab
import pytesseract

# Capture and analyze screen
img = ImageGrab.grab()
data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

print("Words detected:")
for i in range(len(data['text'])):
    word = data['text'][i].strip()
    conf = data['conf'][i]
    if word and conf != '-1':
        print(f"{i:>3}: '{word}' (conf: {conf}) @ ({data['left'][i]}, {data['top'][i]}, {data['width'][i]}, {data['height'][i]})")
