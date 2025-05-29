from pydantic import BaseModel
from datetime import datetime


class ChatMessage(BaseModel):
    content: str
    role: str