from phase_1_clipboard_system.ui_intelligence import UIIntelligence

ui = UIIntelligence()

# Try locating the input field
coords = ui.locate_text("Ask anything")  # or "Type", "Message", etc.

if coords:
    print(f"Found target at: {coords}")
    content = ui.click_and_copy(coords)
    print("Clipboard content:")
    print(content)
    print("Verification:")
    print(ui.verify_clipboard_content(content))
else:
    print("No suitable UI element found.")
