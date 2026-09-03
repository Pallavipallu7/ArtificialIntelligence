from typing import Dict, Any, List

def build_explanation_trace(facts: Dict[str, Any], proof_trace: List[Dict[str, Any]], diagnosis: str, confidence: float) -> Dict[str, Any]:
    """
    Builds a structured expert-system style explanation trace for ticket details UI.
    """
    observed_items = [f"{k} = {v}" for k, v in facts.items() if k not in ["diagnosed_cause", "symptoms"]]

    matched_rules_info = []
    for step in proof_trace:
        antecedent_str = " AND ".join([f"{k} = {v}" for k, v in step.get("antecedents", {}).items()])
        matched_rules_info.append({
            "step": step.get("step"),
            "rule_id": step.get("matched_rule"),
            "rule_statement": f"IF {antecedent_str} THEN {step.get('derived_fact')}",
            "derived_fact": step.get("derived_fact"),
            "confidence": f"{int(step.get('confidence', 0.9) * 100)}%"
        })

    return {
        "observed_symptoms": observed_items,
        "matched_rules": matched_rules_info,
        "probable_cause": diagnosis or "Unknown / Unassigned",
        "confidence": f"{int(confidence * 100)}%",
        "summary": f"Based on observed symptoms ({', '.join(observed_items)}), matched rule '{proof_trace[0]['matched_rule'] if proof_trace else 'N/A'}' derives probable cause: {diagnosis} with {int(confidence*100)}% confidence."
    }
