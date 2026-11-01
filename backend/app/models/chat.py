from typing import Literal
from pydantic import BaseModel

ContentType = Literal[
    "coaching", "linkedin", "instagram", "twitter",
    "email", "training_lesson", "playbook", "framework",
]


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    session_id: str
    message: str
    content_type: ContentType = "coaching"


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    content_type: str
