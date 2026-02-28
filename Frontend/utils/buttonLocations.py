import pyscreeze
import easyocr
import numpy as np
import cv2

# Initialize the reader (English)
# Use gpu=True if you have an NVIDIA card for 10x speed
print("re-initialising reader")
reader = easyocr.Reader(['en'], gpu=True)

def getButtonLocations2():
    # 1. Capture the screen
    screenshot = pyscreeze.screenshot()
    img_np = np.array(screenshot)

    # Downscale image for faster OCR (e.g., 50% size)
    scale_percent = 100
    width = int(img_np.shape[1] * scale_percent / 100)
    height = int(img_np.shape[0] * scale_percent / 100)
    dim = (width, height)
    img_np_small = cv2.resize(img_np, dim, interpolation=cv2.INTER_AREA)

    results = reader.readtext(img_np_small)

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
    prompt_context = "Button Locations on the screen: (NOTE: given format is 'Text_On_Screen button coordinates:'[xcoord, ycoord]). If you wish to click a button, at the start of your prompt, write **click [x,y]**. Find the coords below:"
    for el in elements:
        # We provide the center coordinates to the LLM for easy clicking
        prompt_context += (f"'{el['text']} button coordinates:'[{el['center_x']}, {el['center_y']}], ")

    
    return prompt_context

getButtonLocations()