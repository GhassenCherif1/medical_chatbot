from . import schemas, query_data
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"], 
)

@app.post("/chat")
async def get_response(messages : List[schemas.ChatMessage]):
    return await query_data.query_rag(messages)
