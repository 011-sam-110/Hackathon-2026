import pyscreeze
import easyocr
import numpy as np
import cv2

reader = easyocr.Reader(['en'], gpu=True)

SCALE_PERCENT = 50
SCALE_FACTOR = 100 / SCALE_PERCENT


def _run_ocr():
    screenshot = pyscreeze.screenshot()
    img_np = np.array(screenshot)

    width = int(img_np.shape[1] * SCALE_PERCENT / 100)
    height = int(img_np.shape[0] * SCALE_PERCENT / 100)
    img_small = cv2.resize(img_np, (width, height), interpolation=cv2.INTER_AREA)

    results = reader.readtext(img_small)

    visual_elements = []
    full_text_parts = []

    for (bbox, text, prob) in results:
        top_left = bbox[0]
        bottom_right = bbox[2]

        # Scale coordinates back to real screen positions
        x = int(top_left[0] * SCALE_FACTOR)
        y = int(top_left[1] * SCALE_FACTOR)
        w = int((bottom_right[0] - top_left[0]) * SCALE_FACTOR)
        h = int((bottom_right[1] - top_left[1]) * SCALE_FACTOR)

        center_x = x + (w // 2)
        center_y = y + (h // 2)

        visual_elements.append({
            "text": text,
            "confidence": f"{prob:.2f}",
            "center_x": center_x,
            "center_y": center_y
        })

        full_text_parts.append(text)

    return visual_elements, " ".join(full_text_parts)


def getScreenData():
    """Single OCR pass that returns both button locations string and screen text."""
    elements, screen_text = _run_ocr()

    prompt_context = "Button Locations on the screen: (NOTE: given format is 'Text_On_Screen button coordinates:'[xcoord, ycoord]). If you wish to click a button, at the start of your prompt, write **click [x,y]**. Find the coords below:"
    for el in elements:
        prompt_context += f"'{el['text']} button coordinates:'[{el['center_x']}, {el['center_y']}], "

    return screen_text, prompt_context