from typing import Optional
from pydantic import BaseModel, Field
from app.models.chat import Message


class Session(BaseModel):
    session_id: str
    messages: list[Message] = Field(default_factory=list)
    summary: Optional[str] = None
    turn_count: int = 0


class ConversationHistory(BaseModel):
    messages: list[Message] = Field(default_factory=list)
    summary: Optional[str] = None
