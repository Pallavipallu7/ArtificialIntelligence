from typing import Dict, Any

def format_evaluation_report(dt_metrics: Dict[str, Any], escalation_metrics: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "decision_tree": dt_metrics,
        "escalation_model": escalation_metrics,
        "summary": "AI Decision Tree and Neural Network Escalation models trained and evaluated successfully."
    }
