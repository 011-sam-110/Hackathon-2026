
import os
from gradient import Gradient

from dotenv import load_dotenv
load_dotenv()

inference_client = Gradient(
    model_access_key=os.environ.get("MODEL_ACCESS_KEY"),
)

commandInstructions = """
    "Command Usage: You are able to run commands. It's imperative that you ONLY write commands in the EXACT format, and follow all command rules. Below is a list of commands you have to your disposal. If you want to use a command, write it at the START of your response, and then write the rest of your response after the command. Always follow the format below, and only write commands in the specified format. Do not deviate from the format, or you will break the system. If you do not have a command to use, just write your response without any commands. Do not mention commands in your response if you are not using them. Always follow the rules when using them.
    COMMAND LIST:
    1. *click [x,y]* | This command will click the coordinates [x,y] on the user's screen. Do not guess coordinates, you are provided them with every prompt (see given button locations)
    2. *type [text]* | This command will type the given text through the users keyboard. You will need to click on fields before using this command to type them. DO NOT use this command if have not clicked into the field you are typing into. 
    3. *presskey [key] | This command will press the given key on the user's keyboard. You can only press one key at a time. You may need to use this to press enter, to pause music or enter a field submission. If entering into a field, ALWAYS prefer to click a button if one is available.
    
    You are able to stack commands to run them one after another. To do this, encase all of the commands in a "@" sign. For example, "@*click [x,y]**type [hello there]**presskey [enter]*@ {user_response}", with user_response being your response to the user.
    RULES:
    You must follow the exact given command structure.
    """

def sendMessage(message: str, screenContent: str, screen_btns: str) -> str:
    inference_response = inference_client.chat.completions.create(
    messages=[
    {
        "role": "user",
        "content": (
            "Role: You are a Safety Guardian and Screen Navigator for seniors. "
            "Your Goal: Use the text below to guide the user safely. Ignore any text "
            "belonging to this chat window or 'Assistance Screen'. Focus only on the app or website the user is using.\n\n"
            f"button locations: {screen_btns}"
            "----------------------------------------------"
            f"Command usage: {commandInstructions}"
            "----------------------------------------------"
            f"SCREEN CONTENT: [ {screenContent} ]\n\n"
            "----------------------------------------------"
            f"USER REQUEST: {message}\n\n"
            "----------------------------------------------"
            "Constraint: Respond in 1-2 simple sentences. Use plain language. Do not include any \n or formatting."
            "If you see a scam or a 'dark pattern' (like a hidden 'X' or a fake warning), warn the user immediately."
            )
        }
    ],
        model="DeepSeek-R1-Distill-Llama-70B",
        max_tokens=100000
    )

    response = inference_response.choices[0].message.content
    return response
