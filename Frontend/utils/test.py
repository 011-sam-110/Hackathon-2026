response = {'commands': ['lclick [1064', '799]', 'loop [I clicked the latest release button. Now I need to locate the download button for the latest version.]'], 'message': "I'm helping you download the latest version of Mercurial-Grabber by clicking the latest release button. Next, I'll locate the download button to complete the process."}
response = response['commands']
import re

def parse_ai_response(raw_text: str):
    # 1. Find the block between @ symbols
    command_match = re.search(r'@(.*?)@', raw_text, re.DOTALL)
    
    if command_match:
        command_block = command_match.group(1).strip()
        
        # 2. SMART SPLIT: 
        # This regex says: Split at a comma, but ONLY if the next character 
        # (ignoring spaces) is an asterisk.
        raw_commands = re.split(r',\s*(?=\*)', command_block)
        
        # 3. Clean up the asterisks and whitespace
        commands = [cmd.strip().strip('*') for cmd in raw_commands if cmd.strip()]
        
        # 4. Extract the message
        user_message = re.sub(r'@.*?@', '', raw_text).strip()
        
        return commands, user_message
    
    return [], raw_text.strip()

# --- Testing with your specific broken example ---
raw_ai_input = "@*lclick [1064, 799]*,*loop [I clicked the button]*@ I am helping you..."
commands, message = parse_ai_response(raw_ai_input)

for each in commands:
    print(each)
# Output: ['lclick [1064, 799]', 'loop [I clicked the button]']