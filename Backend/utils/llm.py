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

### COMMAND RULES:
1. ALL commands MUST be wrapped in a single @ block at the VERY START of your response.
2. Format: @*command1*,*command2*,*command3*@
3. If you cannot finish a task in one go (e.g., searching requires seeing the results), you MUST use the *loop [summary]* command as your last command in the stack.
4. If no action is needed, start your response with 'NO_COMMAND'.

### COMMAND LIST:
- *lclick [x,y]* : Left click coordinates.
- *rclick [x,y]* : Right click coordinates (for context menus).
- *type [text]* : Type text (MUST click field first).
- *presskey [key]* : Press a single key (enter, escape, etc.).
- *loop [summary]* : Use this to refresh your view of the screen after an action. Summarize what you did and what you need next.

### EXAMPLE OF SEARCHING & QUEUING:
@*lclick [500,20]*,*type [go with the flow]*,*presskey [enter]*,*loop [I have searched for the song. Now I need to see the results to right-click and queue it.]*@
"""

def parse_ai_response(raw_text: str):
    """
    Extracts the command list and the user-facing message separately.
    """
    # Find everything between the first and last @ symbol
    command_match = re.search(r'@(.*?)@', raw_text, re.DOTALL)
    
    if command_match:
        command_block = command_match.group(1)
        # Split the block by comma and clean up whitespace/asterisks
        commands = [cmd.strip().strip('*') for cmd in command_block.split(',') if cmd.strip()]
        # Remove the @ block from the text to get the clean message for the user
        user_message = re.sub(r'@.*?@', '', raw_text).strip()
        return commands, user_message
    
    return [], raw_text.strip()

def sendMessage(message: str, screenContent: str, screen_btns: str) -> str:
    full_prompt = (
        f"{SYSTEM_GUIDELINES}\n"
        f"--- CURRENT SCREEN STATE ---\n"
        f"BUTTON LOCATIONS: {screen_btns}\n"
        f"SCREEN TEXT CONTENT: {screenContent}\n"
        "-----------------------------\n"
        f"USER REQUEST: {message}\n"
        "-----------------------------\n"
        "Constraint: Provide a concise (max 5 sentences) update for the user after the command block. "
        "Start IMMEDIATELY with the @ block."
    )

    inference_response = inference_client.chat.completions.create(
        messages=[{"role": "user", "content": full_prompt}],
        model="DeepSeek-R1-Distill-Llama-70B",
        max_tokens=4000 # 100k is often too high for standard API calls; 4k is plenty for this.
    )

    raw_content = inference_response.choices[0].message.content
    commands, clean_message = parse_ai_response(raw_content)

    output = {
        "commands": commands,
        "message": clean_message
    }
    print("log info")
    print(output["commands"])
    print(output["message"])
    return output