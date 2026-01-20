from uuid import uuid4
from datetime import datetime
from app.db.mongo import session_collection


def create_or_get_session(user_id: str) -> str:
    """
    If session exists for user_id → return conversation_id
    Else → create new session and return conversation_id
    """

    session = session_collection.find_one(
        {"user_id": user_id, "is_active": True}
    )

    if session:
        return session["conversation_id"]

    conversation_id = str(uuid4())

    session_collection.insert_one({
        "user_id": user_id,
        "conversation_id": conversation_id,
        "created_at": datetime.utcnow(),
        "is_active": True
    })

    return conversation_id

def close_active_session(user_id: str):
    session_collection.update_many(
        {"user_id": user_id, "is_active": True},
        {"$set": {"is_active": False, "ended_at": datetime.utcnow()}}
    )


def create_new_session(user_id:str) -> str:
    conversation_id =str(uuid4())

    session_collection.insert_one({
        "user_id":user_id,
        "conversation_id":conversation_id,
        "created_at":datetime.utcnow(),
        "is_active":True

    })
    return conversation_id