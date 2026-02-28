from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()



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
    
    return {"status": "success", "processed": True}