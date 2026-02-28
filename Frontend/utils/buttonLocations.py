import pyscreeze
import easyocr
import numpy as np

# Initialize the reader (English)
# Use gpu=True if you have an NVIDIA card for 10x speed
reader = easyocr.Reader(['en'], gpu=True)

def getButtonLocations2():
    # 1. Capture the screen
    screenshot = pyscreeze.screenshot()
    img_np = np.array(screenshot)

    # 2. Perform OCR
    results = reader.readtext(img_np)

    visual_elements = []

    for (bbox, text, prob) in results:
        # EasyOCR returns bbox as [[tl], [tr], [br], [bl]]
        top_left = bbox[0]
        bottom_right = bbox[2]
        
        # Original dimensions
        x = int(top_left[0])
        y = int(top_left[1])
        w = int(bottom_right[0] - top_left[0])
        h = int(bottom_right[1] - top_left[1])

        # --- Calculate Center ---
        # Formula: center = start_coordinate + (total_dimension / 2)
        center_x = x + (w // 2)
        center_y = y + (h // 2)

        visual_elements.append({
            "text": text,
            "confidence": f"{prob:.2f}",
            "x": x,
            "y": y,
            "w": w,
            "h": h,
            "center_x": center_x,
            "center_y": center_y
        })

    return visual_elements

def getButtonLocations():
    elements = getButtonLocations2()

    # Format for your LLM
    prompt_context = "Interactable text/buttons found on screen:\n"
    for el in elements:
        # We provide the center coordinates to the LLM for easy clicking
        prompt_context += (f"- '{el['text']}' | Center: [x:{el['center_x']}, y:{el['center_y']}] "
                           f"| Box: {el['w']}x{el['h']}\n")

    print(prompt_context)
    return prompt_context

getButtonLocations()