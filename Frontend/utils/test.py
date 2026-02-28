from pywinauto import Desktop

# Connect to the desktop to see all windows
windows = Desktop(backend="uia").windows()

if windows:
    main_window = windows[0]
    print(f"Searching in: {main_window.window_text()}\n")

    # Find all elements with the 'Button' control type (includes minimize/maximize/close)
    buttons = main_window.descendants(control_type="Button")

    for btn in buttons:
        try:
            rect = btn.rectangle()
            center_x = (rect.left + rect.right) // 2
            center_y = (rect.top + rect.bottom) // 2
            name = btn.window_text() or btn.element_info.name or "(no name)"
            print(f"Button: {name}")
            print(f"  Rectangle: ({rect.left}, {rect.top}) -> ({rect.right}, {rect.bottom})")
            print(f"  Center: ({center_x}, {center_y})")
            if name.lower() in ("minimize", "maximize", "close", "restore"):
                print("  [Title bar button]")
            print()
        except Exception as e:
            print(f"Button (no rect): {btn.window_text()} | Error: {e}\n")