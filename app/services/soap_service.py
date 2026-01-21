from datetime import datetime
from app.db.mongo import (
    session_collection,
    chat_collection,
    soap_collection
)
from app.services.ai_service import generate_medical_response


def generate_soap_report(user_id: str) -> dict:
    # 1. Get active session (✅ MUST be find_one)
    session = session_collection.find_one(
        {"user_id": user_id, "is_active": True}
    )

    if not session:
        raise ValueError("No active conversation found")

    conversation_id = session["conversation_id"]

    # 2. Fetch messages
    messages = list(
        chat_collection.find(
            {"conversation_id": conversation_id}
        ).sort("created_at", 1)
    )

    if not messages:
        raise ValueError("No conversation data available")

    # 3. Build conversation text
    conversation_text = ""
    for msg in messages:
        role = "User" if msg["sender_id"] == "user" else "AI"
        conversation_text += f"{role}: {msg['message']}\n"

    # 4. SOAP prompt
    soap_prompt = f"""
You are a medical documentation assistant.

RULES:
- Do NOT diagnose
- Do NOT prescribe medications
- Use professional, neutral language
- Assessment must be observational
- Plan must recommend consulting a professional

Conversation:
{conversation_text}

Return JSON only:
{{
  "subjective": "...",
  "objective": "...",
  "assessment": "...",
  "plan": "..."
}}
"""

    # 5. Generate SOAP (LLM call)
    soap_report = generate_medical_response(soap_prompt)

    # 6. Save SOAP
    soap_collection.insert_one({
        "user_id": user_id,
        "conversation_id": conversation_id,
        "soap": soap_report,
        "created_at": datetime.utcnow()
    })

    return soap_report
