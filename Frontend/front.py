from calendar import c


import requests
import client
from keyboard import send

import tkinter as tk
import webview
import json
import os
import pyautogui
import time

justLooped = False
loopContext = ""
MAX_LOOP_CONTINUATIONS = 5
COMMAND_DELAY_SECONDS = 1.0
LOOP_SETTLE_SECONDS = 2.5

def parseResponse(raw_text: str):
    #['\n\n', '*lclick [1193,55]*,*type [radiohead]*,*presskey [enter]*,*loop [I have searched for Radiohead. Now I need to see the results to right-click and queue it.]', "  \nI've searched for Radiohead and will queue a song once the results load."]
    print(raw_text)
    parts = raw_text.split("@")
    print(len(parts))
    if len(parts) < 3:
        response = raw_text.strip()
        if len(response) < 5:
            response = "no provided prompt"
        return "", response

    cmds = parts[1]
    response = parts[2].strip()
    print("commands: ", cmds)
    print("response: ", response)
    if len(response) < 5:
        response = "no provided prompt"
    return cmds, response

def rclick(args):
    print("clicking")
    coords = args.split(",")
    pyautogui.click(int(coords[0]), int(coords[1]), button='right')

def click(args):
    print("clicking")
    coords = args.split(",")
    pyautogui.click(int(coords[0]), int(coords[1]))

def dclick(args):
    print("double clicking")
    coords = args.split(",")
    pyautogui.click(int(coords[0]), int(coords[1]), clicks=2)

def hotkey(args):
    coords = args.split(",")
    pyautogui.hotkey(coords[0], coords[1])

def executeCommand(command):
    
    global justLooped, loopContext
#   execute commands here
    command = command.split("[")
    cmd = command[0]
    args = command[1].replace("]","")
    print(cmd, args)

    if cmd.strip() == "lclick":
        click(args)
    elif cmd.strip() == "rclick":
        rclick(args)
    elif cmd.strip() == "dclick":
        dclick(args)
    elif cmd.strip() == "type":
        pyautogui.typewrite(args)
    elif cmd.strip() == "presskey":
        pyautogui.press(args)
    elif cmd.strip() == "hotkey":
        hotkey(args)
    elif cmd.strip() == "loop":
        loopContext = args
        justLooped = True
    elif cmd.strip() == "endloop":
        justLooped = False
    

def unstackCommands(cmds):
    """splits prompts into individuals, and stores in prompts"""
    prompt = cmds.split("*")
    prompts = []
    for each in prompt:
        if len(each) > 3:
            prompts.append(each.strip())
    return prompts


def build_loop_system_prompt(original_question, context):
    return (
        f"ORIGINAL USER REQUEST: {original_question}\n"
        f"LOOP CONTINUATION — The screen has been refreshed with new data.\n"
        f"PREVIOUS ACTIONS: {context}\n"
        "Continue working on the original request above. "
        "If the task is STILL not complete, you MUST end with *loop [summary]*. "
        "If the task IS complete, use *endloop* as your last command."
    )


class Api:
    def ask(self, question):
        global justLooped

        original_question = question
        current_question = question
        response = ""
        continuation_count = 0

        while True:
            returnVal = client.sendQuery(current_question)

            cmds, response = parseResponse(returnVal)

            justLooped = False
            unstackedCommands = unstackCommands(cmds)
            for eachCommand in unstackedCommands:
                executeCommand(eachCommand)
                time.sleep(COMMAND_DELAY_SECONDS)

            if not justLooped:
                break

            continuation_count += 1
            if continuation_count >= MAX_LOOP_CONTINUATIONS:
                response = f"{response}\n\nStopped after {MAX_LOOP_CONTINUATIONS} loop continuations for safety."
                break

            time.sleep(LOOP_SETTLE_SECONDS)
            current_question = build_loop_system_prompt(original_question, loopContext)

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