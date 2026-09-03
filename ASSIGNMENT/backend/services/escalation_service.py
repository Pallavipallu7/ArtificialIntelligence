from typing import Dict, Any
from backend.learning.escalation_model import EscalationRiskModel

def predict_escalation_risk(ticket_data: Dict[str, Any]) -> Dict[str, Any]:
    model = EscalationRiskModel.load()
    if model is None:
        return {
            "escalation_probability": 0.25,
            "risk_level": "LOW",
            "missing_values_handled": True,
            "is_high_risk": False
        }

    return model.predict_risk(ticket_data)
