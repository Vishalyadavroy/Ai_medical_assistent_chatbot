from datetime import datetime
import json
import re
from pydantic import BaseModel
from typing import Dict, Any

from app.db.mongo import (
    session_collection,
    chat_collection,
    soap_collection
)
from app.services.ai_service import generate_medical_response


def extract_json_from_llm(text: str):
    
    if not text:
        return None

  
    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass

    return None


def generate_soap_report(user_id: str):
    
    session = session_collection.find_one(
        {"user_id": user_id, "is_active": True}
    )

    if not session:
        return None

    conversation_id = session["conversation_id"]

    messages = list(
        chat_collection.find(
            {"conversation_id": conversation_id}
        ).sort("created_at", 1)
    )

    if not messages:
        return None


    conversation_text = ""
    for msg in messages:
        role = "User" if msg.get("sender_id") == "user" else "AI"
        conversation_text += f"{role}: {msg.get('message', '')}\n"

    # 4️⃣ SOAP prompt
    soap_prompt = f"""
You are a medical documentation assistant.

RULES:
- Do NOT diagnose
- Do NOT prescribe medications
- Use professional, neutral language
- Assessment must be observational
- Plan must recommend consulting a healthcare professional

Conversation:
{conversation_text}

Return ONLY valid JSON in this format:
{{
  "subjective": "Patient-reported symptoms and concerns",
  "objective": "Observable or measurable findings",
  "assessment": "Clinical impressions (non-diagnostic)",
  "plan": "Recommended next steps (no medication)"
}}
"""

    raw_soap_response = generate_medical_response(soap_prompt)

    print("\n--- RAW LLM SOAP RESPONSE ---\n", raw_soap_response)

    soap_report = extract_json_from_llm(raw_soap_response)

   
    if not soap_report:
        soap_report = {
            "subjective": "Not provided by AI",
            "objective": "Not provided by AI",
            "assessment": "Not provided by AI",
            "plan": "Not provided by AI"
        }

   
    soap_collection.insert_one({
        "user_id": user_id,
        "conversation_id": conversation_id,
        "soap": soap_report,
        "raw_response": raw_soap_response,  
        "created_at": datetime.utcnow()
    })


    return soap_report
