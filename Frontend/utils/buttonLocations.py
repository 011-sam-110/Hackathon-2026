import mss
import numpy as np
import pytesseract as pt

pt.pytesseract.tesseract_cmd = r"C:\Users\sampo\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

MIN_CONFIDENCE = 30


def _run_ocr():
    with mss.mss() as sct:
        mon = sct.monitors[1]
        screenshot = sct.grab(mon)
        img_np = np.array(screenshot)

    data = pt.image_to_data(img_np, output_type=pt.Output.DICT)

    visual_elements = []
    full_text_parts = []

    for i in range(len(data["text"])):
        text = data["text"][i].strip()
        conf = int(data["conf"][i])

        if not text or conf < MIN_CONFIDENCE:
            continue

        x = data["left"][i]
        y = data["top"][i]
        w = data["width"][i]
        h = data["height"][i]

        center_x = x + w // 2
        center_y = y + h // 2

        visual_elements.append({
            "text": text,
            "center_x": center_x,
            "center_y": center_y,
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
