import os
import itertools
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted, PermissionDenied

# ===============================
# CONFIG
# ===============================

SYSTEM_PROMPT = """
You are a medical information assistant.

RULES:
- Do NOT diagnose diseases
- Do NOT prescribe medications
- Do NOT provide treatment plans
- Give only general medical information
- Encourage consulting a licensed medical professional
- Give only general medical information
- Encourage consulting a licensed medical professional
- Be calm, neutral, and professional
"""

API_KEYS = os.getenv("GEMINI_API_KEYS", "").split(",")

key_cycle = itertools.cycle(API_KEYS)



def generate_medical_response(user_message: str) -> str:
   

    for _ in range(len(API_KEYS)):
        api_key = next(key_cycle)

        try:
      
            genai.configure(api_key=api_key)

            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash",
                system_instruction=SYSTEM_PROMPT
            )

            response = model.generate_content(
                user_message,
                generation_config={"temperature": 0.4}
            )

            return response.text

        except (ResourceExhausted, PermissionDenied):
            
            continue

        except Exception:
       
            continue

    return "Service temporarily unavailable. Please try again later."


def ai_generate_soap(chat_text: str):
    return {
        "subjective": "Patient reports symptoms mentioned in chat.",
        "objective": "Based on user-described symptoms only.",
        "assessment": "Possible general causes (no diagnosis).",
        "plan": "General advice, rest, hydration, consult doctor."
    }