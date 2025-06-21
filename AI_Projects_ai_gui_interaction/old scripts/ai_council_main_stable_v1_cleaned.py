#!/usr/bin/env python3
"""
AI Council Main Stable v1 - Based on working version
"""

import time
import pyautogui
import pytesseract
import json
import subprocess
from datetime import datetime

AI_SEQUENCE = [
    {"name": "kai", "desktop": 1, "coords": (504, 790), "read_region": (462, 171, 638, 551)},
    {"name": "claude", "desktop": 2, "coords": (1200, 960), "read_region": (462, 171, 638, 551)},
    {"name": "perplexity", "desktop": 3, "coords": (1200, 960), "read_region": (462, 171, 638, 551)},
    {"name": "grok", "desktop": 4, "coords": (1200, 960), "read_region": (462, 171, 638, 551)},
]

WAIT_AFTER_SEND = 8
OCR_RETRIES = 3
OCR_DELAY = 3
LOOP_DELAY = 15
DEBUG_SAVE_OCR = False

def switch_desktop(number):
    key_code = 17 + number
    script = f'tell application "System Events" to key code {key_code} using control down'
    subprocess.run(["osascript", "-e", script])
    time.sleep(1)

def capture_text(region, ai_name):
    previous = ""
    for attempt in range(OCR_RETRIES):
        pyautogui.scroll(-500)
        time.sleep(1)
        screenshot = pyautogui.screenshot(region=region)
        text = pytesseract.image_to_string(screenshot).strip()
        if DEBUG_SAVE_OCR:
            timestamp = datetime.now().strftime("%H%M%S")
            screenshot.save(f"{ai_name}_ocr_{timestamp}.png")
        if text and text != previous:
            print(f"📜 [{ai_name.upper()}] OCR:\n{text}\n")
            return text
        previous = text
        time.sleep(OCR_DELAY)
    print(f"⚠️ [{ai_name.upper()}] No valid OCR response.")
    return "(No clear reply)"

class AICouncilSession:
    def __init__(self, opening):
        self.history = []
        self.current_message = opening
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.logfile = f"ai_council_log_{now}.json"

    def speak(self, ai):
        print(f"▶️ Switching to {ai['name'].upper()} on Desktop {ai['desktop']}")
        switch_desktop(ai["desktop"])
        pyautogui.click(ai["coords"])
        time.sleep(0.5)
        pyautogui.typewrite(self.current_message)
        pyautogui.press("enter")
        time.sleep(WAIT_AFTER_SEND)

        reply = capture_text(ai["read_region"], ai["name"])
        self.history.append({"from": ai["name"], "message": reply, "timestamp": datetime.now().isoformat()})
        self.current_message = reply

        with open(self.logfile, "w") as f:
            json.dump(self.history, f, indent=2)

def main():
    session = AICouncilSession("Kai, please begin the discussion.")
    while True:
        for ai in AI_SEQUENCE:
            session.speak(ai)
        print("🔄 Loop complete. Waiting...\n")
        time.sleep(LOOP_DELAY)

if __name__ == "__main__":
    main()