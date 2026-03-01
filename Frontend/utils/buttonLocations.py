import mss
import numpy as np
import cv2
import pytesseract as pt

pt.pytesseract.tesseract_cmd = r"C:\Users\sampo\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

MIN_CONFIDENCE = 30
BROWSER_CHROME_HEIGHT = 80
MIN_FIELD_WIDTH = 120
MIN_FIELD_HEIGHT = 20
MAX_FIELD_HEIGHT = 70
MIN_FIELD_ASPECT_RATIO = 2.5
LABEL_PROXIMITY_PX = 80


def _grab_screen():
    with mss.mss() as sct:
        mon = sct.monitors[1]
        screenshot = sct.grab(mon)
        return np.array(screenshot)


def _run_ocr(img_np):
    data = pt.image_to_data(img_np, output_type=pt.Output.DICT)

    text_elements = []
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

        text_elements.append({
            "text": text,
            "center_x": x + w // 2,
            "center_y": y + h // 2,
        })

        full_text_parts.append(text)

    return text_elements, " ".join(full_text_parts)


def _detect_input_fields(img_np):
    """Detect rectangular input fields (text boxes, form fields) via edge/contour detection."""
    gray = cv2.cvtColor(img_np, cv2.COLOR_BGRA2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    kernel = np.ones((3, 3), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    input_fields = []
    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

        if len(approx) < 4:
            continue

        x, y, w, h = cv2.boundingRect(contour)

        if y < BROWSER_CHROME_HEIGHT:
            continue

        aspect_ratio = w / h if h > 0 else 0
        if (w >= MIN_FIELD_WIDTH
                and MIN_FIELD_HEIGHT <= h <= MAX_FIELD_HEIGHT
                and aspect_ratio >= MIN_FIELD_ASPECT_RATIO):
            input_fields.append({
                "center_x": x + w // 2,
                "center_y": y + h // 2,
                "w": w,
                "label": None,
            })

    return input_fields


def _associate_labels(text_elements, input_fields):
    """Match text labels to input fields directly below them."""
    for field in input_fields:
        best_label = None
        best_dist = LABEL_PROXIMITY_PX

        for el in text_elements:
            dy = field["center_y"] - el["center_y"]
            dx = abs(field["center_x"] - el["center_x"])

            if 0 < dy < LABEL_PROXIMITY_PX and dx < field["w"] // 2:
                if dy < best_dist:
                    best_dist = dy
                    best_label = el["text"]

        field["label"] = best_label


def getScreenData():
    """OCR + contour detection: returns screen text and structured element descriptions."""
    img_np = _grab_screen()
    text_elements, screen_text = _run_ocr(img_np)
    input_fields = _detect_input_fields(img_np)
    _associate_labels(text_elements, input_fields)

    parts = []

    parts.append("CLICKABLE TEXT on screen (buttons, links, menu items):")
    for el in text_elements:
        parts.append(f"  '{el['text']}' at [{el['center_x']}, {el['center_y']}]")

    if input_fields:
        parts.append("INPUT FIELDS on screen (text boxes — click here BEFORE using *type*):")
        for field in input_fields:
            label = field["label"] or "unlabeled"
            parts.append(
                f"  [{label}] input field at [{field['center_x']}, {field['center_y']}]"
            )

    return screen_text, "\n".join(parts)
