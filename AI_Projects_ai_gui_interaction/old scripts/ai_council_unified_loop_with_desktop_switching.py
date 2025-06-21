#!/usr/bin/env python3
"""
AI Council Unified Loop with Desktop Switching
"""

import time
import pyautogui
import pytesseract
import json
import subprocess
from datetime import datetime

# Define AI participants in order
AI_ORDER = [
    {"name": "kai", "desktop": 1, "coords": (504, 790), "read_region": (462, 171, 638, 551)},
    {"name": "claude", "desktop": 2, "coords": (1200, 960), "read_region": (462, 171, 638, 551)},
    {"name": "perplexity", "desktop": 3, "coords": (1200, 960), "read_region": (462, 171, 638, 551)},
    {"name": "grok", "desktop": 4, "coords": (1200, 960), "read_region": (462, 171, 638, 551)},
]

WAIT_AFTER_SEND = 8
OCR_RETRIES = 3
OCR_DELAY = 3
ROUND_DELAY = 15

def switch_desktop(desktop_number):
    # Maps 1 → key code 18, 2 → 19, ..., 9 → 26
    key_code = 17 + desktop_number
    script = f'''
    tell application "System Events"
        key code {key_code} using control down
    end tell
    '''
    subprocess.run(["osascript", "-e", script])

class AICouncil:
    def __init__(self, initial_message):
        self.last_message = initial_message
        self.session_log = []
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_file = f"ai_council_session_{now}.json"

    def send_to_ai(self, ai, message):
        print(f"📨 [{ai['name'].upper()}] Sending message...")
        switch_desktop(ai["desktop"])
        time.sleep(1)
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
                print(f"📜 [{ai['name'].upper()}] OCR Detected:\n{text}")
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
        print("🔁 Round complete. Restarting in 15 seconds...\n")
        time.sleep(ROUND_DELAY)

if __name__ == "__main__":
    main()