from datetime import datetime
from app.db.mongo import chat_collection


def save_message(
    user_id: str,
    conversation_id: str,
    sender_id: str,
    receiver_id: str,
    message: str
):
    created_at = datetime.utcnow()

    chat_collection.insert_one({
        "user_id": user_id,
        "conversation_id": conversation_id,
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "message": message,
        "created_at": created_at
    })

    return created_at


from app.db.mongo import chat_collection


def fetch_conversation_history(user_id: str, conversation_id: str):
    chats = chat_collection.find(
        {
            "user_id": user_id,
            "conversation_id": conversation_id
        }
    ).sort("created_at", 1)  # 1 = ascending (old → new)

    history = []

    for chat in chats:
        history.append({
            "sender_id": chat["sender_id"],
            "receiver_id": chat["receiver_id"],
            "message": chat["message"],
            "created_time": chat["created_at"]
        })

    return history



