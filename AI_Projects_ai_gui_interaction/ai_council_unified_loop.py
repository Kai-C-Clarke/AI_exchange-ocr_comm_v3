#!/usr/bin/env python3
"""
AI Council Unified Loop
- Based on stable core from main_working.py
- Enhanced with pattern-aware OCR, smart retry logic, and infinite loop
- Clean logging and structured response handling
"""

import time
import pyautogui
import pytesseract
import json
from datetime import datetime

# Define AI participants in order
AI_ORDER = [
    {"name": "kai", "desktop": 1, "coords": (504, 790), "read_region": (462, 171, 638, 551)},
    {"name": "claude", "desktop": 1, "coords": (1200, 960), "read_region": (462, 171, 638, 551)},
    {"name": "perplexity", "desktop": 1, "coords": (1200, 960), "read_region": (462, 171, 638, 551)},
    {"name": "grok", "desktop": 1, "coords": (1200, 960), "read_region": (462, 171, 638, 551)},
]

WAIT_AFTER_SEND = 8
OCR_RETRIES = 3
OCR_DELAY = 3
ROUND_DELAY = 15

class AICouncil:
    def __init__(self, initial_message):
        self.last_message = initial_message
        self.session_log = []
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_file = f"ai_council_session_{now}.json"

    def send_to_ai(self, ai, message):
        print(f"📨 [{ai['name'].upper()}] Sending message...")
        pyautogui.click(ai["coords"])
        time.sleep(0.5)
        pyautogui.typewrite(message)
        pyautogui.press("enter")
        time.sleep(WAIT_AFTER_SEND)

    def capture_ocr_response(self, ai):
        region = ai["read_region"]
        print(f"🔎 [{ai['name'].upper()}] Capturing screen for OCR...")
        previous_text = ""
        for attempt in range(OCR_RETRIES):
            pyautogui.scroll(-500)
            time.sleep(1)
            screenshot = pyautogui.screenshot(region=region)
            text = pytesseract.image_to_string(screenshot).strip()
            if text and text != previous_text:
                print(f"📜 [{ai['name'].upper()}] OCR Detected:
{text}")
                return text
            previous_text = text
            time.sleep(OCR_DELAY)
        print(f"⚠️ [{ai['name'].upper()}] No clear OCR response detected.")
        return "(No clear reply)"

    def log_response(self, ai_name, message):
        entry = {"from": ai_name, "message": message, "timestamp": datetime.now().isoformat()}
        self.session_log.append(entry)
        with open(self.session_file, "w") as f:
            json.dump(self.session_log, f, indent=2)

    def loop_once(self):
        for ai in AI_ORDER:
            self.send_to_ai(ai, self.last_message)
            reply = self.capture_ocr_response(ai)
            self.log_response(ai["name"], reply)
            self.last_message = reply

def main():
    initial_prompt = "Kai, please begin the discussion."
    council = AICouncil(initial_prompt)
    while True:
        council.loop_once()
        print("🔁 Round complete. Restarting in 15 seconds...
")
        time.sleep(ROUND_DELAY)

if __name__ == "__main__":
    main()