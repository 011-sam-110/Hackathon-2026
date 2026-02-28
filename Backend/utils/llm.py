
import os
from gradient import Gradient

from dotenv import load_dotenv
load_dotenv()

print(os.environ.get("MODEL_ACCESS_KEY"))
def sendMessage(message: str, screenContent: str) -> str:
    
    


    inference_client = Gradient(
        model_access_key=os.environ.get(
            "MODEL_ACCESS_KEY"
        ),
    )

    inference_response = inference_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"You are a helpful assistant that helps people find information on there screen. Below is all of the text on their screen. You must use this to figure out what is happening on the users end {screenContent}. Keep responses 1-2 sentances"
            }
        ],
        model="openai-gpt-oss-120b",
        max_tokens=1000
    )

    return inference_response.choices[0].message.content
