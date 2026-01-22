from pydantic import BaseModel
from datetime import datetime
from typing import List
from typing import Dict, Any

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    user_id: str
    conversation_id: str
    sender_id: str
    receiver_id: str
    message: str
    created_time: datetime

class ChatMessage(BaseModel):
    sender_id: str
    receiver_id: str
    message: str
    created_time: datetime


class ChatHistoryResponse(BaseModel):
    user_id: str
    conversation_id: str
    messages: List[ChatMessage]


# class SOAPResponse(BaseModel):
#     soap_report: Dict[str, Any]
#     disclaimer:str


class SOAPData(BaseModel):
    subjective: str
    objective: str
    assessment: str
    plan: str


class SOAPResponse(BaseModel):
    soap_report: SOAPData
    disclaimer: str