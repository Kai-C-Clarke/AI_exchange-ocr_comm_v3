import time
import logging
from core.config import UI_CONFIGS, WAIT_BEFORE_CAPTURE
from core.ocr_filter import clean_ocr_output, process_multiple_frames
from core.utils import scroll_area_and_capture_text

def scroll_and_capture(ui: str):
    logging.info(f"🖼️  Capturing response from {ui}...")
    time.sleep(WAIT_BEFORE_CAPTURE)  # Let UI settle before capture

    text_blocks = []
    region = UI_CONFIGS[ui]["scroll_region"]
    
    # Capture fewer frames but with better processing
    for frame in range(3):  # Reduced from 6 to 3 frames
        raw = scroll_area_and_capture_text(region)
        logging.info(f"[{ui} Frame {frame}] Raw OCR length: {len(raw)} chars")
        
        # Only add if we got substantial text
        if len(raw.strip()) > 15:  # Minimum threshold
            cleaned = clean_ocr_output(raw)
            if len(cleaned.strip()) > 10:
                logging.info(f"[{ui} Frame {frame}] Cleaned: '{cleaned[:60]}...'")
                text_blocks.append(cleaned)
        
        # Small scroll between frames to get different content
        if frame < 2:  # Don't scroll after last frame
            import pyautogui
            pyautogui.scroll(-2, x=region[0] + 50, y=region[1] + 50)
            time.sleep(0.8)  # Reduced wait time between frames

    if not text_blocks:
        logging.warning(f"⚠️ No readable text captured from {ui}")
        return "[No readable text]", 0, "Empty after OCR"

    # Process all frames together for best result
    final_text = process_multiple_frames(text_blocks)
    
    logging.info(f"🧾 OCR completed for {ui}: {len(text_blocks)} frame(s) processed")
    logging.info(f"📄 Final result: '{final_text}'")
    
    return final_text, len(text_blocks), "Captured"

def quick_capture(ui: str):
    """Alternative function for single-frame capture when speed is needed."""
    logging.info(f"⚡ Quick capture from {ui}...")
    
    region = UI_CONFIGS[ui]["scroll_region"]
    raw = scroll_area_and_capture_text(region)
    cleaned = clean_ocr_output(raw)
    
    if len(cleaned.strip()) < 10:
        return "[No readable text]", 1, "Empty"
    
    logging.info(f"⚡ Quick result: '{cleaned}'")
    return cleaned, 1, "Quick captured"