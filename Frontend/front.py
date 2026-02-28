import requests
import client
from keyboard import send

import tkinter as tk
import webview
import client
import json
import os
import pyautogui

def click(cmd):
    _, coords = cmd.split(" ")
    coords = coords.replace("[","").replace("]","").split(",")
    pyautogui.click(int(coords[0]), int(coords[1]))

def extractCMD(prompt):
    try:
        cmd,prompt = prompt.split("*")[1:3]
        return cmd.strip(), prompt.strip()
    
    except Exception as e:
        return None, prompt.strip()
class Api:
    def ask(self, question):
        if not question:
            return {"response": "Please enter a question."}
        ai_response = client.sendQuery(question)
        cmd, prompt = extractCMD(ai_response)
        if cmd != None:
            if "click" in cmd:
                click(cmd)

        return {"response": prompt}

def get_html_path():
    return os.path.join(os.path.dirname(__file__), "index.html")

if __name__ == "__main__":
    api = Api()
    window = webview.create_window(
        "THE NAVIGATOR",
        url=get_html_path(),
        js_api=api,
        width=370,
        height=800,
        resizable=False
    )
    webview.start(debug=True)