from typing import Optional

from pydantic import BaseModel


class MessageResponse(BaseModel):
    content: str


class ChatResponse(BaseModel):
    messages: list[MessageResponse]
    conversation_id: str


class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str


class DescriptionReq(BaseModel):
    name: str
    brand: str
    category: str
    primary_keyword: str
    secondary_keywords: list[str]
    target_audence: list[str]
