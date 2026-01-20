#This is where cookiers and response are handle 
from fastapi import APIRouter, Request , Response ,HTTPException
from uuid import uuid4
from app.services.session_service import create_or_get_session
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import save_message
from app.services.ai_service import generate_medical_response
from app.services.chat_service import fetch_conversation_history
from app.schemas.chat import ChatHistoryResponse
from app.services.session_service import close_active_session ,create_new_session

router = APIRouter(prefix="/chatbot" , tags=["AI Chatbot"])


@router.post("/chat")

def init_chat(request:Request , response:Response):
    #1= check cookies
    user_id = request.cookies.get("user_id")

    #2=if cookies not found -> genrate and set 
    if not user_id:
        user_id=str(uuid4())
        #this send cookie to browser , browser auto-attaches next time
        response.set_cookie(
            key="user_id",
            value=user_id,
            httponly=True,
            samesite="lax"
        )

    #3=create or get session
    conversation_id = create_or_get_session(user_id)

    return{
        "user_id":user_id,
        "converstation_id":conversation_id
    }


@router.post("/chat/message", response_model=ChatResponse)
def send_message(request: Request, chat: ChatRequest):
    user_id = request.cookies.get("user_id")

    if not user_id:
        raise HTTPException(status_code=400, detail="Session not initialized")

    conversation_id = create_or_get_session(user_id)

    # 1 Save USER → AI message
    save_message(
        user_id=user_id,
        conversation_id=conversation_id,
        sender_id=user_id,
        receiver_id="medical_ai",
        message=chat.message
    )

    # 2 Generate AI response
    ai_message = generate_medical_response(chat.message)

    # 3 Save AI → USER message and get timestamp
    created_time = save_message(
        user_id=user_id,
        conversation_id=conversation_id,
        sender_id="medical_ai",
        receiver_id=user_id,
        message=ai_message
    )

    # 4 Return AI response metadata
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
    user_id = request.cookies.get("user_id")

    if not user_id:
        raise HTTPException(status_code=400, detail="Session not initialized")

    # 1️⃣ Close existing conversation
    close_active_session(user_id)

    # 2️⃣ Create new conversation
    conversation_id = create_new_session(user_id)

    return {
        "user_id": user_id,
        "conversation_id": conversation_id,
        "message": "New conversation started"
    }
