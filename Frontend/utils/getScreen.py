from os import read
import mss
from PIL import Image
import pytesseract as pt
import cv2
import numpy as np

def getScreenText():
    with mss.mss() as sct:
        # Capture monitor 1
        monitor_number = 1
        mon = sct.monitors[monitor_number]

        monitor = {
            "top": mon["top"],
            "left": mon["left"],
            "width": mon["width"],
            "height": mon["height"],
            "mon": monitor_number,
        }

        # Grab screen
        sct_img = sct.grab(monitor)

        # Convert to NumPy (BGRA → BGR)
        img = np.array(sct_img)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # Save screenshot
        cv2.imwrite("screen.png", img)
        return read_text(img)

def read_text(img):
    pt.pytesseract.tesseract_cmd = r"C:\\Users\\sampo\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"
    text = pt.image_to_string(img)
    return text