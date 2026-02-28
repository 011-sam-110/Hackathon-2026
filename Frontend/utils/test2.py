import time
from pywinauto import Desktop

print("Click on your Browser window NOW... (3 seconds)")
time.sleep(3)

# 1. Get the Desktop object
desktop = Desktop(backend="uia")

# 2. Get the actual active window (the one you just clicked)
# top_window() is more reliable for 'active' than indexing windows()
try:
    window = desktop.top_window()
    print(f"Targeting active window: {window.window_text()}")

    # 3. Use descendants with a filter instead of child_window
    # This is more resilient to the 'UIAWrapper' attribute issue
    all_elements = window.descendants(control_type="Document")
    
    if not all_elements:
        print("No 'Document' (web content) found. Trying to find all buttons in the whole window instead...")
        buttons = window.descendants(control_type="Button")
    else:
        # Use the first Document found (the webpage)
        web_content = all_elements[0]
        buttons = web_content.descendants(control_type="Button")

    # 4. Extract Coordinates
    for btn in buttons:
        name = btn.window_text() or "Unnamed/Icon"
        rect = btn.rectangle()
        mid = rect.mid_point()
        print(f"Button: {name:20} | Center: ({mid.x}, {mid.y})")

except Exception as e:
    print(f"An error occurred: {e}")