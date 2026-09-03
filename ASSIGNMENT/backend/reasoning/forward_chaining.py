from typing import Dict, Any, List, Tuple
from backend.reasoning.kb import KnowledgeBase, Rule

def forward_chain(kb: KnowledgeBase, facts: Dict[str, Any], max_iterations: int = 20) -> Tuple[Optional[str], float, List[Dict[str, Any]], Dict[str, Any]]:
    """
    Executes forward chaining on the Knowledge Base given initial facts.
    Returns: (diagnosed_cause, confidence, proof_trace, updated_facts)
    """
    current_facts = facts.copy()
    proof_trace = []
    visited_rules = set()
    diagnosed_cause = None
    confidence = 0.0

    step_count = 0
    active_rules = sorted(kb.get_active_rules(), key=lambda r: r.priority, reverse=True)

    for iteration in range(max_iterations):
        rule_fired = False
        for rule in active_rules:
            if rule.rule_id in visited_rules:
                continue

            if rule.matches(current_facts):
                rule_fired = True
                visited_rules.add(rule.rule_id)
                step_count += 1

                # Calculate confidence based on antecedents count & rule priority
                antecedent_count = len(rule.antecedents)
                base_confidence = 0.85 + min(0.10, antecedent_count * 0.03)
                confidence = round(base_confidence, 2)
                diagnosed_cause = rule.consequent

                # Record proof trace step
                proof_trace.append({
                    "step": step_count,
                    "matched_rule": rule.rule_id,
                    "rule_category": rule.category,
                    "antecedents": rule.antecedents,
                    "derived_fact": rule.consequent,
                    "confidence": confidence
                })

                # Add consequent to derived facts
                current_facts["diagnosed_cause"] = rule.consequent
                current_facts[f"derived_{rule.rule_id}"] = True
                break  # Fired highest priority matching rule in this pass

        if not rule_fired or diagnosed_cause:
            break

    return diagnosed_cause, confidence, proof_trace, current_facts
