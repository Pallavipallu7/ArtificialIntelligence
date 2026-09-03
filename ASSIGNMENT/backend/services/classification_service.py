from typing import Dict, Any
from backend.learning.decision_tree import TicketDecisionTreeModel

def classify_ticket_category_priority(ticket_data: Dict[str, Any]) -> Dict[str, Any]:
    model = TicketDecisionTreeModel.load()
    if model is None:
        # Fallback heuristic if un-trained
        dept = ticket_data.get("department", "CSE")
        symptoms = ticket_data.get("symptoms", {})
        if "ac" in str(symptoms).lower():
            category = "AC_POWER"
        elif "projector" in str(symptoms).lower():
            category = "PROJECTOR_LAMP"
        elif "wifi" in str(symptoms).lower():
            category = "WIFI_NO_CONNECTIVITY"
        else:
            category = "OTHER_INFRASTRUCTURE"
        return {"category": category, "priority": "HIGH", "confidence": 0.85}

    return model.predict(ticket_data)
