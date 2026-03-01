from calendar import c


import requests
import client
from keyboard import send

import tkinter as tk
import webview
import client
import json
import os
import pyautogui


def parseResponse(raw_text: str):
    #['\n\n', '*lclick [1193,55]*,*type [radiohead]*,*presskey [enter]*,*loop [I have searched for Radiohead. Now I need to see the results to right-click and queue it.]', "  \nI've searched for Radiohead and will queue a song once the results load."]
    print(raw_text)
    raw_text = raw_text.split("@")
    print(len(raw_text))
    cmds = raw_text[0]
    response = raw_text[1]
    print("commands: ", cmds)
    print("response: ", response)
    return [cmds, response]

        

class Api:
    def ask(self, question):
        returnVal = client.sendQuery(question)
        
        response = parseResponse(returnVal)
        print(f"AI full response: {response}")
        print("Command list:")

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