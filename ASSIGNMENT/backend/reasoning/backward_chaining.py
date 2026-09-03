from typing import Dict, Any, List, Tuple
from backend.reasoning.kb import KnowledgeBase, Rule

# Human-readable question mapping for facts
QUESTION_MAP = {
    "power_indicator": "Is the power indicator on the device ON or OFF?",
    "remote_no_response": "Does the remote control respond when pressed?",
    "compressor_no_sound": "Is the AC compressor completely silent without any sound?",
    "cooling_low": "Is the cooling level low or ineffective?",
    "ac_water_leak": "Is water leaking or dripping from the AC unit?",
    "projector_no_display": "Is the projector failing to display any image?",
    "lamp_led": "What is the status of the projector Lamp LED (off, on, or blinking)?",
    "power_led": "Is the projector Power LED on or off?",
    "lamp_hours": "How many hours has the projector lamp been used?",
    "wifi_no_connectivity": "Are devices completely unable to connect to the Wi-Fi network?",
    "router_led": "Is the Wi-Fi router status LED on or off?",
    "multiple_users_affected": "Are multiple users in the area experiencing this problem?",
    "single_user_affected": "Is only a single user device affected?",
    "lab_equipment_no_power": "Is the laboratory equipment failing to power on?",
    "socket_tested_ok": "Has the wall power socket been tested and confirmed working?",
    "lighting_flicker": "Are the lights flickering continuously?",
    "recently_installed": "Was this light fixture or component recently installed?",
    "classroom_ac_noisy": "Is the classroom AC making excessive noise?",
    "vibration_present": "Is noticeable vibration coming from the unit?"
}

def backward_chain(kb: KnowledgeBase, current_facts: Dict[str, Any]) -> Tuple[List[str], List[str], List[Dict[str, Any]]]:
    """
    Executes goal-driven backward chaining to find candidate rules that partially match.
    Returns: (missing_facts, generated_questions, candidate_rules_info)
    """
    candidate_rules = []
    missing_facts_set = set()

    for rule in kb.get_active_rules():
        # Check partial overlap
        satisfied_count = 0
        conflicting = False
        missing_antecedents = []

        for k, v in rule.antecedents.items():
            fact_key = k[:-3] if k.endswith(("_gt", "_lt")) else k
            if fact_key in current_facts:
                # Test match
                if k.endswith("_gt"):
                    fact_val = current_facts[fact_key]
                    if isinstance(fact_val, (int, float)) and fact_val > v:
                        satisfied_count += 1
                    else:
                        conflicting = True
                elif k.endswith("_lt"):
                    fact_val = current_facts[fact_key]
                    if isinstance(fact_val, (int, float)) and fact_val < v:
                        satisfied_count += 1
                    else:
                        conflicting = True
                else:
                    fact_val = current_facts[fact_key]
                    if isinstance(v, bool):
                        if bool(fact_val) == v:
                            satisfied_count += 1
                        else:
                            conflicting = True
                    elif isinstance(v, str):
                        if str(fact_val).strip().lower() == str(v).strip().lower():
                            satisfied_count += 1
                        else:
                            conflicting = True
                    else:
                        if fact_val == v:
                            satisfied_count += 1
                        else:
                            conflicting = True
            else:
                missing_antecedents.append(fact_key)

        # If partially satisfied (at least 1 antecedent matched) and no direct contradiction
        if satisfied_count > 0 and not conflicting and missing_antecedents:
            candidate_rules.append({
                "rule_id": rule.rule_id,
                "consequent": rule.consequent,
                "satisfied_count": satisfied_count,
                "missing_antecedents": missing_antecedents
            })
            for m in missing_antecedents:
                missing_facts_set.add(m)

    # If no antecedents were matched at all, look for general category context rules
    if not candidate_rules:
        # Collect most common initial facts to query
        for rule in sorted(kb.get_active_rules(), key=lambda r: r.priority, reverse=True):
            for k in rule.antecedents.keys():
                fact_key = k[:-3] if k.endswith(("_gt", "_lt")) else k
                if fact_key not in current_facts:
                    missing_facts_set.add(fact_key)

    missing_facts_list = list(missing_facts_set)
    questions = [
        QUESTION_MAP.get(fact, f"Could you provide information for '{fact}'?")
        for fact in missing_facts_list
    ]

    return missing_facts_list, questions, candidate_rules
