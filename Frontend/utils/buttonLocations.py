import pyscreeze
import easyocr
import numpy as np

# Initialize the reader (English)
# Use gpu=True if you have an NVIDIA card for 10x speed
reader = easyocr.Reader(['en'], gpu=False)

def getButtonLocations():
    # 1. Capture the screen
    screenshot = pyscreeze.screenshot()
    # Convert PIL image to a format EasyOCR/OpenCV understands (numpy array)
    img_np = np.array(screenshot)

    # 2. Perform OCR
    # detail=1 gives us the coordinates; 0 would give just text
    results = reader.readtext(img_np)

    visual_elements = []

    for (bbox, text, prob) in results:
        # EasyOCR returns bbox as [[tl], [tr], [br], [bl]]
        top_left = bbox[0]
        bottom_right = bbox[2]
        
        # Calculate width and height
        width = bottom_right[0] - top_left[0]
        height = bottom_right[1] - top_left[1]

        visual_elements.append({
            "text": text,
            "confidence": f"{prob:.2f}",
            "x": int(top_left[0]),
            "y": int(top_left[1]),
            "w": int(width),
            "h": int(height)
        })

    return visual_elements

# --- Execution ---
elements = getButtonLocations()

# Format for your LLM
prompt_context = "Buttons on screen:\n"
for el in elements:
    prompt_context += f"- '{el['text']}' at [x:{el['x']}, y:{el['y']}] (Size: {el['w']}x{el['h']})\n"

print(prompt_context)