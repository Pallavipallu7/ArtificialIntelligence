import re
from typing import Tuple

INTENT_KEYWORDS = {
    "check_status": ["ticket", "status", "where is", "tkt-", "track", "complaint", "progress"],
    "report_fault": ["ac", "projector", "wifi", "network", "lab", "equipment", "light", "fan", "broken", "not working", "fault", "issue", "leak", "flicker", "noisy", "dim"],
    "ask_help": ["help", "how to", "info", "contact", "support", "services", "guide"],
    "provide_symptom": ["yes", "no", "on", "off", "blinking", "silent", "low", "high", "indicator", "compressor", "remote", "display", "router", "flickering"]
}

OUT_OF_SCOPE_PATTERNS = [
    "capital of", "weather", "poem", "recipe", "who is", "joke", "meaning of life",
    "tell me a story", "write code", "movie", "song"
]

def classify_intent(message: str, in_dialogue_state: bool = False) -> str:
    text = message.lower().strip()

    # Check out-of-scope first (TC10 compliance)
    for pattern in OUT_OF_SCOPE_PATTERNS:
        if pattern in text:
            return "unknown"

    # Ticket status lookup check
    if re.search(r"tkt-\d+", text) or "where is my ticket" in text or "status of" in text:
        return "check_status"

    # If currently in dialogue flow collecting symptoms and user gives affirmative/negative/short answers
    if in_dialogue_state:
        if text in ["yes", "no", "on", "off", "blinking", "silent", "high", "low"] or len(text.split()) <= 4:
            return "provide_symptom"

    # Match keywords
    scores = {intent: 0 for intent in INTENT_KEYWORDS}
    words = text.split()
    for word in words:
        for intent, kw_list in INTENT_KEYWORDS.items():
            if word in kw_list or any(kw in text for kw in kw_list):
                scores[intent] += 1

    best_intent = max(scores, key=scores.get)
    if scores[best_intent] == 0:
        return "unknown"

    return best_intent
