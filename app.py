from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from starlette import status

from llm_functions.chat import think, demo_think
from supabase_functions.add_embedding_to_db import convert_and_add_data_to_supabase
import validators

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:4001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/hello")
def read_hello():
    return {"message": "Hello from FastAPI"}


class ChatModelSchema(BaseModel):
    message: str
    # user_id: str = "19882d24-8e26-4407-9ba0-daf0546b8200"
    file_id: str = "19882d24-8e26-4407-9ba0-daf0546b8200"
    model: str = "gpt-4o"
    session_id: str = "19882d24-8e26-4407-9ba0-daf0546b8200"


@app.post("/chat_model")
async def chat_model(chat: ChatModelSchema):
    try:
        return StreamingResponse(think(chat.message, chat.file_id, chat.model, chat.session_id), media_type='text/event-stream')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


class DemoChatModelSchema(BaseModel):
    message: str


@app.post("/demo_chat_model")
async def demo_chat_model(chat: DemoChatModelSchema):
    try:
        return StreamingResponse(demo_think(chat.message), media_type='text/event-stream')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

