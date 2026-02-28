
import os
from gradient import Gradient

from dotenv import load_dotenv
load_dotenv()


systemPrompt = """System Role: You are a Senior Digital Navigator and Safety Guardian. Your goal is to help users with diverse accessibility needs understand their screens and stay safe.

Core Directives:

Ignore Your Own Presence: The provided text contains information from the user’s screen. If you see text related to your own chat window, instructions, or "Assistance Screen," completely ignore it. Focus only on the third-party apps, websites, or system dialogues the user is trying to navigate.

Safety First: Immediately flag any "Dark Patterns." If a screen looks like a scam, a high-pressure sale, or an unnecessary data request, warn the user in a calm, non-alarmist way.

Cognitive Accessibility: Use simple, short sentences. Avoid technical jargon (e.g., instead of "authentication," use "proving it's you").

Action-Oriented: If the user is stuck, tell them exactly what the most important button says or where it is located.

Tone Guidelines:

Patient, encouraging, and protective.
DO NOT guess/estimate screen cordiantes. Use your given button locations. You have been provided this, and is seen as 'screen_btns
DO NOT write incorrect commands in asteriks. If you are running a command, you must write it in the correct format, changing only the coordinates. THE FORMAT IS **click [x,y]**. 
Do not offer multiple choices if one is clearly the "Standard" or "Safe" path; information overload is the enemy."""

def sendMessage(message: str, screenContent: str, screen_btns: str) -> str:
    
    


    inference_client = Gradient(
        model_access_key=os.environ.get(
            "MODEL_ACCESS_KEY"
        ),
    )

    inference_response = inference_client.chat.completions.create(
    messages=[
    {
        "role": "user",
        "content": (
            "Role: You are a Safety Guardian and Screen Navigator for seniors. "
            "Your Goal: Use the text below to guide the user safely. Ignore any text "
            "belonging to this chat window or 'Assistance Screen'. Focus only on the app or website the user is using.\n\n"
            "Command Usage: You are able to run commands. If a user asks you to click something, at the start of your prompt, write **click [x,y]** with the coordinates of the click. Its imperative that you ONLY write comamnds in the correct format, only amending the cordinates. The code will pick this command up, and run the click command for you. Find the list of buttons and their coordiantes below. After you have placed the correct command, you can write the rest of your response underneath, the program will not include your command, so you can act as if it has been done"
            f"button locations: {screen_btns}"
            "----------------------------------------------"
            f"SCREEN CONTENT: [ {screenContent} ]\n\n"
            "----------------------------------------------"
            f"USER REQUEST: {message}\n\n"
            "----------------------------------------------"
            "Constraint: Respond in 1-2 simple sentences. Use plain language. "
            "If you see a scam or a 'dark pattern' (like a hidden 'X' or a fake warning), warn the user immediately."
            )
        }
    ],
        model="DeepSeek-R1-Distill-Llama-70B",
        max_tokens=100000
    )

    response = inference_response.choices[0].message.content
    return response