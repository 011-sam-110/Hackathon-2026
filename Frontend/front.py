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
        returnVal = client.sendQuery(question)

        cmds, response = returnVal
        print(f"AI full response: {response}")
        print("Command list:")
        for each in cmds:
            print(each)
        return {"response": response}

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