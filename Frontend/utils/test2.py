command = "presskey [enter]"

import pyautogui
import time

def rclick(args):
    print("clicking")
    coords = args.split(",")
    pyautogui.click(int(coords[0]), int(coords[1]), button='right')

def click(args):
    print("clicking")
    coords = args.split(",")
    pyautogui.click(int(coords[0]), int(coords[1]))

def executeCommand(command):
    
#   execute commands here
    command = command.split("[")
    cmd = command[0]
    args = command[1].replace("]","")
    print(cmd, args)

    if cmd.strip() == "lclick":
        click(args)
    elif cmd.strip() == "rclick":
        rclick(args)
    elif cmd.strip() == "type":
        pyautogui.typewrite(args)
    elif cmd.strip() == "presskey":
        pyautogui.press(args)
    elif cmd.strip() == "loop":
        pass
    

time.sleep(1)
executeCommand(command)