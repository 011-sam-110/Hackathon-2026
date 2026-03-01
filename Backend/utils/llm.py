from curses import raw
import os
import re
from gradient import Gradient
from dotenv import load_dotenv

load_dotenv()

# Initialize Gradient Client
inference_client = Gradient(
    model_access_key=os.environ.get("MODEL_ACCESS_KEY"),
)

# --- STRICT PROMPT CONFIGURATION ---
SYSTEM_GUIDELINES = """
Role: You are a Safety Guardian and Screen Navigator for seniors.
Goal: Complete the user's task using the provided command list. 

### UNDERSTANDING THE SCREEN DATA:
The screen data contains TWO types of elements:
1. CLICKABLE TEXT: These are visible text labels, buttons, links, and menu items. Use their coordinates for clicking buttons or links.
2. INPUT FIELDS: These are text boxes where you can type. They are labeled with the name of the field (e.g. [Username], [Password]).

IMPORTANT: When you need to TYPE into a form field, you MUST click on the INPUT FIELD coordinates, NOT on the text label above it. Text labels are just descriptions — the input field is the actual box you type into.

### COMMAND RULES:
1. ALL commands MUST be wrapped in a single @ block at the VERY START of your response.
2. Format: @*command1*,*command2*,*command3*@
3. If you cannot finish a task in one go (e.g., searching requires seeing the results), you MUST use the *loop [summary]* command as your LAST command in the stack. This is MANDATORY.
4. If no action is needed, start your response with 'NO_COMMAND'.
5. ALL X,Y coordinates MUST be filled in, and CANNOT be left blank or with placeholders. If you do not know the coordinates, you MUST use the loop command to get more information.
6. YOU MUST log all of your previous prompts and what you were trying to achieve. 

### COMMAND LIST:
- *lclick [x,y]* : Left click coordinates.
- *rclick [x,y]* : Right click coordinates (for context menus).
- *dclick [x,y]* : Double click coordinates (sometimes needed to open files or folders, or for playing songs)
- *type [text]* : Type text (MUST click an INPUT FIELD first, not a text label).
- *presskey [key]* : Press a single key (enter, escape, etc.).
- *loop [summary]* : Use this to refresh your view of the screen after an action. Summarize what you did and what you need next.
- *hotkey [firstkey,secondkey]* : Use this to execute a hotkey (e.g., ctrl+k to search on spotify).
- *endloop [placeholder]* : Use this to end a loop once your task is completed. 

### EXAMPLE — Filling a login form:
Screen shows: [Username] input field at [510, 410], [Password] input field at [510, 478], 'Submit' at [359, 533]
User asks: "Log in with username admin and password secret"
@*lclick [510,410]*,*type [admin]*,*lclick [510,478]*,*type [secret]*,*lclick [359,533]*,*loop [Clicked username input field, typed admin, clicked password input field, typed secret, clicked Submit. Need to check if login succeeded.]*@
I've entered the credentials and clicked Submit. Checking if the login went through.

### SOME ADVICE:
- If you want to search for a song on spotify, you can run *hotkey [ctrl,k]* to open the search bar without needing to know the coordinates. You will then be able to type the song name/artist. You can then loop to find the song title, and then click that button. 
- If you find yourself in a prompt loop without achieving the task, try to change your approach by clicking a different, related button.
- When attempting to play a song, double click it.
- NEVER click on instructional text or labels when you need to type — ALWAYS use the INPUT FIELD coordinates.

### CRITICAL REMINDER:
If the task requires more than one step and is NOT fully complete, your LAST command MUST be *loop [summary]*. NEVER omit the loop command when additional steps are still needed.
"""

    
def sendMessage(message: str, screenContent: str, screen_btns: str, history: list = None) -> dict:
    user_prompt = (
        f"--- CURRENT SCREEN STATE ---\n"
        f"SCREEN ELEMENTS:\n{screen_btns}\n"
        f"SCREEN TEXT CONTENT: {screenContent}\n"
        "-----------------------------\n"
        f"USER REQUEST: {message}\n"
        "-----------------------------\n"
        "Provide a concise (max 5 sentences) update for the user after the command block. "
        "Start IMMEDIATELY with the @ block. "
        "REMEMBER: If the task is not fully complete, your LAST command MUST be *loop [summary]*."
    )

    messages = [{"role": "system", "content": SYSTEM_GUIDELINES}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_prompt})

    inference_response = inference_client.chat.completions.create(
        messages=messages,
        model="GPT-4o",
        max_tokens=4000,
    )

    raw_content = inference_response.choices[0].message.content
    print(f"Raw LLM response: {raw_content}")

    return {"response": raw_content, "user_prompt_used": user_prompt}