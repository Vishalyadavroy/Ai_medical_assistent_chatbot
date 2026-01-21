import re

CRITICAL_KEYWORDS = [
    # Heart / Chest
    "heart attack",
    "heart pain",
    "chest pain",
    "chest tightness",
    "pressure in chest",
    "pain in chest",

    # Breathing
    "shortness of breath",
    "breathing problem",
    "difficulty breathing",
    "can't breathe",
    "cannot breathe",

    # Radiating pain
    "left arm pain",
    "jaw pain",
    "shoulder pain",

    # Neurological / collapse
    "collapse",
    "unconscious",
    "fainted",
    "stroke",
    "seizure",

    # Bleeding
    "severe bleeding",
    "heavy bleeding"
]


def contains_critical_medical_issue(message: str) -> bool:
    message = message.lower().strip()

    return any(keyword in message for keyword in CRITICAL_KEYWORDS)

    return False







def emergency_response() -> str:
    """
    Emergency-safe response (NO medical advice)
    """
    return (
        " **Medical Emergency Detected** \n\n"
        "I’m really sorry,\n\n"
        "-  **India Emergency Number:** 112\n"
        "- Call a local ambulance service immediately\n"
        "-  Go to the **nearest hospital or emergency department**\n\n"
    )
