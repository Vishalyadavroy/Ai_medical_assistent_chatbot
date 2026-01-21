# ============================================================
# Chatbot Routes
# Handles:
# - Cookies & sessions
# - Chat messages
# - Emergency medical filtering
# - Chat history
# - New conversation
# - SOAP report
# ============================================================

from fastapi import APIRouter, Request, Response, HTTPException
from uuid import uuid4

# ---------- Schemas ----------
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ChatHistoryResponse,
    SOAPResponse
)

# ---------- Services ----------
from app.services.session_service import (
    create_or_get_session,
    close_active_session,
    create_new_session
)
from app.services.chat_service import (
    save_message,
    fetch_conversation_history
)
from app.services.ai_service import generate_medical_response
from app.services.soap_service import generate_soap_report
from app.services.medical_filter import (
    contains_critical_medical_issue,
    emergency_response
)

# ---------- Database ----------
from app.db.mongo import chat_collection

# ---------- Router ----------
router = APIRouter(prefix="/chatbot", tags=["AI Chatbot"])

@router.post("/chat")
def init_chat(request: Request, response: Response):
    """
    Initializes user session using cookies.
    Creates a new user_id if not present.
    """

    user_id = request.cookies.get("user_id")

    if not user_id:
        user_id = str(uuid4())
        response.set_cookie(
            key="user_id",
            value=user_id,
            httponly=True,
            samesite="lax"
        )

    conversation_id = create_or_get_session(user_id)

    return {
        "user_id": user_id,
        "conversation_id": conversation_id
    }

@router.post("/chat/message", response_model=ChatResponse)
def send_message(request: Request, chat: ChatRequest):
    """
    Handles user → AI message flow
    Includes critical medical emergency filtering
    """

    user_id = request.cookies.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="Session not initialized")

    conversation_id = create_or_get_session(user_id)
    user_message = chat.message.strip()

    # ---------- Save USER message ----------
    save_message(
        user_id=user_id,
        conversation_id=conversation_id,
        sender_id=user_id,
        receiver_id="medical_ai",
        message=user_message
    )

    # ---------- Emergency Medical Filter ----------
    if contains_critical_medical_issue(user_message):
        ai_message = emergency_response()

    else:
        # ---------- Safe LLM Response ----------
        ai_message = generate_medical_response(user_message)

    # ---------- Save AI message ----------
    created_time = save_message(
        user_id=user_id,
        conversation_id=conversation_id,
        sender_id="medical_ai",
        receiver_id=user_id,
        message=ai_message
    )

    return {
        "user_id": user_id,
        "conversation_id": conversation_id,
        "sender_id": "medical_ai",
        "receiver_id": user_id,
        "message": ai_message,
        "created_time": created_time
    }

@router.get("/chat/history", response_model=ChatHistoryResponse)
def get_chat_history(request: Request):
    """
    Returns chat history for active conversation
    """

    user_id = request.cookies.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="Session not initialized")

    conversation_id = create_or_get_session(user_id)

    messages = fetch_conversation_history(
        user_id=user_id,
        conversation_id=conversation_id
    )

    return {
        "user_id": user_id,
        "conversation_id": conversation_id,
        "messages": messages
    }

@router.post("/chat/new")
def start_new_chat(request: Request):
    """
    Closes active conversation and starts a new one
    """

    user_id = request.cookies.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="Session not initialized")

    close_active_session(user_id)
    conversation_id = create_new_session(user_id)

    return {
        "user_id": user_id,
        "conversation_id": conversation_id,
        "message": "New conversation started"
    }

@router.get("/soap", response_model=SOAPResponse)
def get_soap_report(request: Request):
    """
    Generates SOAP report from chat history
    """

    user_id = request.cookies.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="Session not initialized")

    soap_report = generate_soap_report(user_id)

    return SOAPResponse(
        soap_report=soap_report,
        disclaimer=(
            "This SOAP report is generated for educational purposes only "
            "and is not a medical diagnosis."
        )
    )
