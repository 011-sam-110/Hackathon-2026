import pyautogui

prompt = "I have clicked that for you"

def extractCMD(prompt):
    try:
        cmd,prompt = prompt.split("*")[1:3]
        return cmd.strip(), prompt.strip()
    
    except Exception as e:
        return None, prompt.strip()

cmd = "click [1438,670]"

click(cmd)