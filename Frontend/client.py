import requests, os
from dotenv import load_dotenv
from utils.buttonLocations import getScreenData

load_dotenv()
NGROK_URL = os.getenv("NGROK_URL")

def sendQuery(userPrompt, history=None):
    screenText, buttonLocations = getScreenData()
    payload = {
        "user_prompt": userPrompt,
        "screen_text": screenText,
        "screen_btns": buttonLocations,
        "history": history,
    }
    print("-" * 50)
    response = requests.post(
        f"{NGROK_URL}/upload-text",
        json=payload,
    )
    print(response)
    try:
        data = response.json()
        return {
            "response": data.get("response", response.text),
            "user_prompt_used": data.get("user_prompt_used", ""),
        }
    except Exception:
        return {"response": response.text, "user_prompt_used": ""}

if __name__ == "__main__":
    sendQuery("What is on my screen?")