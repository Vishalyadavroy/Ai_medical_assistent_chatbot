import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


SYSTEM_PROMPT = """
You are a medical information assistant.

RULES:
- Do NOT diagnose diseases
- Do NOT prescribe medications
- Do NOT provide treatment plans
- Give only general medical information
- Encourage consulting a licensed medical professional
- Be calm, neutral, and professional
"""


def generate_medical_response(user_message: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content":SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content

def ai_generate_soap(chat_text: str):
    return {
        "subjective": "Patient reports symptoms mentioned in chat.",
        "objective": "Based on user-described symptoms only.",
        "assessment": "Possible general causes (no diagnosis).",
        "plan": "General advice, rest, hydration, consult doctor."
    }
