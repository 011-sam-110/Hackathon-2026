import pyautogui

prompt = '"\n\n*click [223,523]*  \nClicked on Liked Songs for you."'

def extractCMD(prompt):
    try:
        prompt = prompt.split("*")[1:3]
        print(prompt)
        return prompt[0].strip(), prompt[1].strip()
    except Exception as e:
        return None, prompt.strip()

cmd, prompt = extractCMD(prompt)

print(f"Extracted command: {cmd}, Remaining prompt: {prompt}")
def click(cmd):
    print("clicking")
    _, coords = cmd.split(" ")
    coords = coords.replace("[","").replace("]","").split(",")
    pyautogui.click(int(coords[0]), int(coords[1]))

click(cmd)

