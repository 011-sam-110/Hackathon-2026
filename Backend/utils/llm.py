
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
    1. *lclick [x,y]* | This command will left click the coordinates [x,y] on the user's screen. Do not guess coordinates, you are provided them with every prompt (see given button locations)
    2. *type [text]* | This command will type the given text through the users keyboard. You will need to click on fields before using this command to type them. DO NOT use this command if have not clicked into the field you are typing into. 
    3. *presskey [key] | This command will press the given key on the user's keyboard. You can only press one key at a time. You may need to use this to press enter, to pause music or enter a field submission. If entering into a field, ALWAYS prefer to click a button if one is available.
    4. *rclick [x,y]* | This command will right click the coordinates [x,y] on the user's screen. Use this command to open context menus or interact with elements that require right click (such as queuing songs on spotify)
    5. *loop [summary]* | This command is the most important command, and allows you to prompt yourself. If you cannot complete a task due to not having enough information (e.g not knowing what the next button is) you can run this. You MUST give a summary of what you have done, and what you are now trying to achieve. The new prompt will then re-gather all the information (screen content, button locations) and give it to you, along with your summary. This allows you to "loop" and gather new information, allowing you to complete tasks that require multiple steps. Always give a detailed summary of what you have done, and what you are trying to do next, so that when you loop, you can get the most relevant information for your next step. If you find yourself stuck or needing more information, use this command to loop and gather more information.

    RULES:
    YOU MUST follow the exact given command structure, ensuring to encase all commands in asteriks, and ALWAYS stacking commands if you cannot complete the action in one task. 
    You are able to stack commands to run them one after another. To do this, encase all of the commands in a "@" sign. For example, "@*click [x,y]*,*type [hello there]*,*presskey [enter]*@ {user_response}", with user_response being your response to the user.

    
    Extra hints:
    How can i queue a song? you can queue a song by first left clicking the search box labelled "what do you want to play?" or similar. You can then right click on the song you want to queue, and click the "add to queue" or similar button. 
    How do i figure other things out? Ask yourself, how do i queue a song on spotify? and then program this in the given commandlist.
    """

def sendMessage(message: str, screenContent: str, screen_btns: str) -> str:
    inference_response = inference_client.chat.completions.create(
    messages=[
    {
        "role": "user",
        "content": (
            "Role: You are a Safety Guardian and Screen Navigator for seniors. "
            "Your Goal: Complete the task the user gives you, and ensure the users safety ensuring all websites are safe. "
            "belonging to this chat window or 'Assistance Screen'. Focus only on the app or website the user is using. Ensure you follow proper command usage whenever you would like to perform an action on behalf of the same user.\n\n"
            f"button locations: {screen_btns}"
            "----------------------------------------------"
            f"Command usage: {commandInstructions}"
            "----------------------------------------------"
            f"SCREEN CONTENT: [ {screenContent} ]\n\n"
            "----------------------------------------------"
            f"USER REQUEST: {message}\n\n"
            "----------------------------------------------"
            "Constraint: You must follow correct command usage whenever you want to perform an action. Whether you decide to run a command or not, you must always give an instructive, concise step-by-step instruction of what they should do, or what you have done for them. This should be at most 5-6 sentances long, unless longer is required."
            "If you see a scam or a 'dark pattern' (like a hidden 'X' or a fake warning), warn the user immediately. YOU MUST ALWAYS put commands at the start of the prompt"
            )
        }
    ],
        model="DeepSeek-R1-Distill-Llama-70B",
        max_tokens=100000
    )

    response = inference_response.choices[0].message.content
    return response