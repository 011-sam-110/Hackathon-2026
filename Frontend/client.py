import requests, os
from dotenv import load_dotenv
from utils.buttonLocations import getScreenData

load_dotenv()
NGROK_URL = os.getenv("NGROK_URL")
def sendQuery(userPrompt):
    screenText, buttonLocations = getScreenData()
    payload = {
        "user_prompt": userPrompt, 
        "screen_text": screenText,
        "screen_btns": buttonLocations,
    }
    print("-"*50)
    response = requests.post(
        f"{NGROK_URL}/upload-text", 
        json=payload
    )
    print(response)
    try:
        # Try to get JSON response with 'response' key
        data = response.json()
        if 'response' in data:
            return data['response']
        return response.text
    except Exception:
        return response.text
    
if __name__ == "__main__":
    sendQuery("What is on my screen?")