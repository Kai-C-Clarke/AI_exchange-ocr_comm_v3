#!/usr/bin/env python3
"""
AI Council Input System – Final Version with OCR Watch, Scroll, and Safe Logging
"""

import time
import pyautogui
import pytesseract

class AICouncilInputSystem:
    def __init__(self):
        self.session_log = []

    def send_message_to_ai(self, ai_name, message, method, coords, desktop):
        # Pre-log session entry
        log_entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "ai": ai_name,
            "message": message,
            "method": method,
            "coordinates": coords,
            "desktop": desktop,
            "status": "sent",
            "ocr_response": None
        }
        self.session_log.append(log_entry)

        print(f"📤 Sending to {ai_name}")
        time.sleep(1)  # Simulate switching desktop and focusing input
        print(f"🧠 Typing method: {method} at {coords}")
        print(f"💬 Message: {message}")

        # Fake typing/paste
        pyautogui.click(coords)
        time.sleep(0.5)
        pyautogui.typewrite(message)
        pyautogui.press("enter")

        # Add scroll step for verbose AIs
        if ai_name in ["finn", "perplexity"]:
            pyautogui.moveTo(coords[0], coords[1] - 200)
            pyautogui.scroll(-500)

        # Response wait loop
        print("⏳ Waiting for OCR-visible response...")
        last_text = ""
        for _ in range(30):
            screenshot = pyautogui.screenshot(region=(462, 171, 638, 551))
            text = pytesseract.image_to_string(screenshot).strip()
            if text and text != last_text:
                print(f"📜 OCR Detected:
{text}")
                self.session_log[-1]["ocr_response"] = text
                break
            time.sleep(1)
            last_text = text
        else:
            print("⚠️ OCR timeout: No new response found.")
            self.session_log[-1]["ocr_response"] = "No response within time window."

def main():
    system = AICouncilInputSystem()
    # Example test call
    system.send_message_to_ai("claude", "Test from Council", "applescript", (1200, 960), 1)

if __name__ == "__main__":
    main()