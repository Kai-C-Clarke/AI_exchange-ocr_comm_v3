import pyautogui
import pyperclip
import time

def click_near_input_region():
    screen_width, screen_height = pyautogui.size()
    x = screen_width // 2
    y = int(screen_height * 0.93)  # Adjust if needed
    print(f"Clicking at: ({x}, {y})")

    pyautogui.click(x, y)
    time.sleep(0.2)
    pyautogui.hotkey('command', 'a')
    pyautogui.hotkey('command', 'c')
    time.sleep(0.2)

    clipboard_content = pyperclip.paste()
    return clipboard_content

if __name__ == "__main__":
    print("Running relative click test...")
    content = click_near_input_region()
    print("Clipboard content:\n")
    print(content)
