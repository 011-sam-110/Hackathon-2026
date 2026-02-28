import json
import os
import openai

from dotenv import load_dotenv
load_dotenv()



def sendMessage(message: str, screenContent: str) -> str:

    conversationConfig = [
    {
        "role": "system",
        "content": f"You are a helpful assistant that helps people find information on there screen. Below is all of the text on their screen. You must use this to figure out what is happening on the users end {screenContent}. Keep responses 1-2 sentances"
    }
    ]
    conversation = conversationConfig
    conversation.append({"role": "user", "content": message})
    
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation,
        temperature=0.8,
        max_tokens=150
    )
    
    # Access content as an attribute, not a dict
    assistant_message = response.choices[0].message.content
    
    conversation.append({"role": "assistant", "content": assistant_message})
    
    return assistant_message