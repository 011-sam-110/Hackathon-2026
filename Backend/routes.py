from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
app = FastAPI(title="My API", description="This is a sample API", version="1.0.0")
from utils import llm
import logging


LOG = logging.getLogger(__name__)
LOG.info("API is starting up")
LOG.info(uvicorn.Config.asgi_version)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/response")
def get_response():
    return {"response": "This is a response"}

@app.get("/runcmd")
def get_response():
    return {"response": "This is a response"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
class LargeTextData(BaseModel):
    user_prompt: str
    screen_text: str

@app.post("/upload-text")
def receive_text(data: LargeTextData):
    print(f"User said: {data.user_prompt}")
    print(f"Screen contained {len(data.screen_text)} characters")
    
    response = llm.sendMessage(data.user_prompt, data.screen_text)

    LOG.info(f"LLM response: {response}")
    return response