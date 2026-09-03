from typing import List, Dict, Any, Optional

DEFAULT_RULES = [
    {
        "rule_id": "R1",
        "category": "AC_POWER",
        "antecedents": {"power_indicator": "off", "remote_no_response": True},
        "consequent": "Power supply failure",
        "priority": 10,
        "active": True
    },
    {
        "rule_id": "R2",
        "category": "AC_COOLING",
        "antecedents": {"power_indicator": "on", "compressor_no_sound": True, "cooling_low": True},
        "consequent": "Compressor fault",
        "priority": 9,
        "active": True
    },
    {
        "rule_id": "R3",
        "category": "AC_WATER_LEAK",
        "antecedents": {"ac_water_leak": True},
        "consequent": "Drainage blockage",
        "priority": 8,
        "active": True
    },
    {
        "rule_id": "R4",
        "category": "PROJECTOR_LAMP",
        "antecedents": {"projector_no_display": True, "lamp_led": "blinking"},
        "consequent": "Lamp failure",
        "priority": 9,
        "active": True
    },
    {
        "rule_id": "R5",
        "category": "PROJECTOR_POWER",
        "antecedents": {"projector_no_display": True, "power_led": "off"},
        "consequent": "Power cable fault",
        "priority": 8,
        "active": True
    },
    {
        "rule_id": "R6",
        "category": "PROJECTOR_LAMP",
        "antecedents": {"projector_image_dim": True, "lamp_hours_gt": 3000},
        "consequent": "Lamp end-of-life",
        "priority": 7,
        "active": True
    },
    {
        "rule_id": "R7",
        "category": "ROUTER_POWER",
        "antecedents": {"wifi_no_connectivity": True, "router_led": "off"},
        "consequent": "Router power failure",
        "priority": 9,
        "active": True
    },
    {
        "rule_id": "R8",
        "category": "NETWORK_SLOW",
        "antecedents": {"wifi_intermittent": True, "multiple_users_affected": True},
        "consequent": "Bandwidth congestion",
        "priority": 7,
        "active": True
    },
    {
        "rule_id": "R9",
        "category": "WIFI_NO_CONNECTIVITY",
        "antecedents": {"wifi_no_connectivity": True, "router_led": "on", "single_user_affected": True},
        "consequent": "Device configuration issue",
        "priority": 8,
        "active": True
    },
    {
        "rule_id": "R10",
        "category": "LAB_EQUIPMENT_INTERNAL",
        "antecedents": {"lab_equipment_no_power": True, "socket_tested_ok": True},
        "consequent": "Equipment internal fault",
        "priority": 9,
        "active": True
    },
    {
        "rule_id": "R11",
        "category": "LIGHTING_FLICKER",
        "antecedents": {"lighting_flicker": True, "recently_installed": True},
        "consequent": "Faulty ballast/driver",
        "priority": 7,
        "active": True
    },
    {
        "rule_id": "R12",
        "category": "AC_NOISE",
        "antecedents": {"classroom_ac_noisy": True, "vibration_present": True},
        "consequent": "Loose mounting / fan imbalance",
        "priority": 7,
        "active": True
    }
]

class Rule:
    def __init__(self, rule_id: str, category: str, antecedents: Dict[str, Any], consequent: str, priority: int = 1, active: bool = True):
        self.rule_id = rule_id
        self.category = category
        self.antecedents = antecedents
        self.consequent = consequent
        self.priority = priority
        self.active = active

    def matches(self, facts: Dict[str, Any]) -> bool:
        """Check if all antecedents are satisfied by facts."""
        if not self.active:
            return False

        for k, v in self.antecedents.items():
            # Handle special numeric comparator like lamp_hours_gt
            if k.endswith("_gt"):
                base_k = k[:-3]
                fact_val = facts.get(base_k)
                if fact_val is None or not (isinstance(fact_val, (int, float)) and fact_val > v):
                    return False
            elif k.endswith("_lt"):
                base_k = k[:-3]
                fact_val = facts.get(base_k)
                if fact_val is None or not (isinstance(fact_val, (int, float)) and fact_val < v):
                    return False
            else:
                if k not in facts:
                    return False
                fact_val = facts[k]
                # Normalize booleans and strings
                if isinstance(v, bool):
                    if bool(fact_val) != v:
                        return False
                elif isinstance(v, str):
                    if str(fact_val).strip().lower() != str(v).strip().lower():
                        return False
                else:
                    if fact_val != v:
                        return False
        return True

class KnowledgeBase:
    def __init__(self, rules: Optional[List[Rule]] = None):
        if rules is None:
            self.rules = [Rule(**r) for r in DEFAULT_RULES]
        else:
            self.rules = rules

    def get_active_rules(self) -> List[Rule]:
        return [r for r in self.rules if r.active]

    def add_rule(self, rule: Rule):
        self.rules.append(rule)

    def remove_rule(self, rule_id: str):
        self.rules = [r for r in self.rules if r.rule_id != rule_id]

    def update_rule(self, rule_id: str, **kwargs):
        for r in self.rules:
            if r.rule_id == rule_id:
                for k, v in kwargs.items():
                    if hasattr(r, k) and v is not None:
                        setattr(r, k, v)
