import pyautogui
import time
import logging
from core.config import UI_CONFIGS

def safe_click_area(ai_name):
    if ai_name not in UI_CONFIGS:
        raise ValueError(f"No config found for {ai_name}")
    x, y = UI_CONFIGS[ai_name]["safe_click"][0]
    pyautogui.moveTo(x, y)
    pyautogui.click()
    time.sleep(0.5)
    logging.info(f"🖱️ Clicked into {ai_name}'s safe area at ({x},{y})")

def switch_to_desktop(n):
    if n == 1:
        pyautogui.hotkey('ctrl', 'left')
    elif n == 2:
        pyautogui.hotkey('ctrl', 'right')
    time.sleep(1.5)
    logging.info(f"🧭 Switched to Desktop {n}")

