import requests
import client
from keyboard import send

import tkinter as tk
import webview
import client
import json
import os
import pyautogui




class Api:
    def ask(self, question):
        ai_response = client.sendQuery(question)

        print(f"AI full response: {ai_response}")



        return {"response": ai_response}

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