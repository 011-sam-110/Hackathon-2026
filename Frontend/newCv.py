import os
import json
import base64
import pyautogui
from openai import OpenAI
from PIL import ImageGrab, ImageDraw

# 1. Setup Client
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

def capture_screen_with_grid(step=100):
    """Captures screen and draws a grid to help GPT-4o with spatial reasoning."""
    screenshot = ImageGrab.grab()
    width, height = screenshot.size
    draw = ImageDraw.Draw(screenshot)
    
    # Draw grid lines & labels
    for x in range(0, width, step):
        draw.line([(x, 0), (x, height)], fill="red", width=1)
        draw.text((x + 5, 5), str(x), fill="red")
    for y in range(0, height, step):
        draw.line([(0, y), (width, y)], fill="red", width=1)
        draw.text((5, y + 5), str(y), fill="red")
        
    screenshot.save("current_screen.png")
    return "current_screen.png"

def get_coordinates_from_gpt(prompt):
    """Sends screenshot to GPT-4o and asks for specific pixel coordinates."""
    with open("current_screen.png", "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system", 
                "content": "You are a computer control agent. Look at the screenshot with the red grid. "
                           "Identify the (x, y) coordinates of the UI element requested. "
                           "Return ONLY a JSON object: {\"x\": int, \"y\": int, \"reason\": string}"
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Find the coordinates to: {prompt}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                ]
            }
        ],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

def execute_action(action_data):
    """Moves the mouse and clicks based on AI reasoning."""
    x, y = action_data['x'], action_data['y']
    print(f"Moving to ({x}, {y}) - Reason: {action_data['reason']}")
    
    # Smooth movement is more reliable in complex UIs
    pyautogui.moveTo(x, y, duration=0.5)
    pyautogui.click()

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    user_request = "Open the Spotify icon on my taskbar and press play"
    
    # 1. See
    capture_screen_with_grid()
    
    # 2. Think
    coords = get_coordinates_from_gpt(user_request)
    
    # 3. Act
    execute_action(coords)