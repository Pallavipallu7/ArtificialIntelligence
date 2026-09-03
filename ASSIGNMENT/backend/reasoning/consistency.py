from typing import List, Dict, Any, Tuple
from backend.reasoning.kb import KnowledgeBase, Rule

def detect_contradictions(kb: KnowledgeBase, facts: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Detects contradictions where multiple active rules match the same facts
    or subset of facts but lead to conflicting conclusions (TC03 compliance).
    """
    matching_rules = []
    for rule in kb.get_active_rules():
        if rule.matches(facts):
            matching_rules.append(rule)

    contradictions = []
    if len(matching_rules) > 1:
        # Check if matched rules lead to distinct consequents
        consequents = set(r.consequent for r in matching_rules)
        if len(consequents) > 1:
            contradictions.append({
                "type": "CONTRADICTORY_CONCLUSIONS",
                "message": f"Multiple rules matched current facts but yielded conflicting conclusions: {list(consequents)}",
                "matched_rules": [r.rule_id for r in matching_rules],
                "consequents": list(consequents)
            })

    # Also check KB static inconsistency: identical antecedents with different consequent
    active_rules = kb.get_active_rules()
    for i in range(len(active_rules)):
        for j in range(i + 1, len(active_rules)):
            r1, r2 = active_rules[i], active_rules[j]
            if r1.antecedents == r2.antecedents and r1.consequent != r2.consequent:
                contradictions.append({
                    "type": "STATIC_KB_CONTRADICTION",
                    "message": f"Rules {r1.rule_id} and {r2.rule_id} have identical antecedents but conflicting conclusions.",
                    "matched_rules": [r1.rule_id, r2.rule_id],
                    "consequents": [r1.consequent, r2.consequent]
                })

    return contradictions

def detect_circular_dependencies(kb: KnowledgeBase) -> List[Tuple[str, str]]:
    """
    Analyzes rule antecedent-consequent dependencies to detect circular loops A -> B -> A.
    """
    cycles = []
    # Build graph: consequent -> rule antecedents
    # Check if consequent of one rule appears as antecedent of another
    for r1 in kb.get_active_rules():
        for r2 in kb.get_active_rules():
            if r1.rule_id != r2.rule_id:
                # Check if r1 consequent is referenced in r2 antecedents and vice-versa
                r1_cons_key = r1.consequent.lower().replace(" ", "_")
                if r1_cons_key in r2.antecedents:
                    r2_cons_key = r2.consequent.lower().replace(" ", "_")
                    if r2_cons_key in r1.antecedents:
                        cycles.append((r1.rule_id, r2.rule_id))
    return cycles
