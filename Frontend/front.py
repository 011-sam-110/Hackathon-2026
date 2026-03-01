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
    print("clicking")
    _, xcord, ycord = cmd.split()
    
    xcord = xcord.replace("[","").replace(",","")
    ycord = ycord.replace("]","")
    pyautogui.click(int(xcord), int(ycord))

def extractCMD(prompt):
    try:
        cmd,prompt = prompt.split("*")[1:3]
        return cmd.strip(), prompt.strip().replace('"','').replace("n","").replace("/","")
    
    except Exception as e:
        return None, prompt.strip()
class Api:
    def ask(self, question):
        ai_response = client.sendQuery(question)

        print(f"AI full response: {ai_response}")
        cmds, prompt = extractCMD(ai_response)
        print(f"commands: {cmds}, prompt: {prompt}")

#AI full response: {"commands":["lclick [2532,1281]","loop [I have clicked on the \"play songs from radiohead, a\" button. I need to see if the action was successful and if the songs are loading.]"],"message":""}


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