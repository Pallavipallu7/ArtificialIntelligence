import numpy as np
import random
from typing import List, Dict, Any, Tuple

DEFAULT_STAFF_MEMBERS = [
    {"id": 1, "name": "Arun Kumar", "department": "CSE", "skills": ["AC_POWER", "AC_COOLING", "PROJECTOR_POWER"], "workload": 2, "avg_res_time": 4.0},
    {"id": 2, "name": "Priya Sharma", "department": "ECE", "skills": ["WIFI_NO_CONNECTIVITY", "ROUTER_POWER", "NETWORK_SLOW"], "workload": 1, "avg_res_time": 3.5},
    {"id": 3, "name": "Rajesh Verma", "department": "EEE", "skills": ["LIGHTING_FLICKER", "CLASSROOM_POWER", "LAB_EQUIPMENT_POWER"], "workload": 4, "avg_res_time": 5.0},
    {"id": 4, "name": "Sneha Patel", "department": "Mechanical", "skills": ["AC_WATER_LEAK", "AC_NOISE", "CLASSROOM_FAN"], "workload": 2, "avg_res_time": 4.5},
    {"id": 5, "name": "Vikram Singh", "department": "Biotechnology", "skills": ["LAB_EQUIPMENT_INTERNAL", "EQUIPMENT_OVERHEATING"], "workload": 3, "avg_res_time": 6.0},
    {"id": 6, "name": "Ananya Reddy", "department": "General", "skills": ["PROJECTOR_DISPLAY", "PROJECTOR_LAMP", "OTHER_INFRASTRUCTURE"], "workload": 1, "avg_res_time": 3.0}
]

CATEGORIES = [
    "AC_POWER", "AC_COOLING", "AC_WATER_LEAK", "AC_NOISE",
    "PROJECTOR_DISPLAY", "PROJECTOR_LAMP", "PROJECTOR_POWER",
    "WIFI_NO_CONNECTIVITY", "WIFI_INTERMITTENT", "ROUTER_POWER",
    "LAB_EQUIPMENT_POWER", "LAB_EQUIPMENT_INTERNAL",
    "LIGHTING_FLICKER", "LIGHTING_FAILURE",
    "CLASSROOM_POWER", "CLASSROOM_FAN", "CLASSROOM_SOCKET",
    "NETWORK_SLOW", "EQUIPMENT_OVERHEATING", "OTHER_INFRASTRUCTURE"
]

PRIORITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

def get_workload_bucket(workload: int) -> str:
    if workload <= 1:
        return "LIGHT"
    elif workload <= 3:
        return "MODERATE"
    else:
        return "HEAVY"

class HelpdeskRoutingEnv:
    def __init__(self, staff_list: List[Dict[str, Any]] = None):
        self.staff_list = staff_list or [s.copy() for s in DEFAULT_STAFF_MEMBERS]
        self.num_actions = len(self.staff_list)
        self.lambda_penalty = 1.5

    def reset_workloads(self):
        for s in self.staff_list:
            s["workload"] = random.randint(0, 3)

    def sample_state(self) -> Tuple[str, str, str]:
        cat = random.choice(CATEGORIES)
        prio = random.choice(PRIORITIES)
        avg_w = int(np.mean([s["workload"] for s in self.staff_list]))
        w_bucket = get_workload_bucket(avg_w)
        return (cat, prio, w_bucket)

    def step(self, state: Tuple[str, str, str], action_staff_index: int) -> Tuple[Tuple[str, str, str], float, Dict[str, Any]]:
        staff = self.staff_list[action_staff_index]
        cat, prio, _ = state

        # Skill match factor
        has_skill = cat in staff.get("skills", [])
        dept_match = staff.get("department") in [cat.split("_")[0], "General"]

        base_res_time = staff["avg_res_time"]
        if not has_skill:
            base_res_time += 3.0
        if not dept_match:
            base_res_time += 1.5

        # Priority modifier
        prio_mult = {"LOW": 0.8, "MEDIUM": 1.0, "HIGH": 1.3, "CRITICAL": 1.6}.get(prio, 1.0)
        actual_res_time = base_res_time * prio_mult + (staff["workload"] * 0.8)

        # Update workload
        staff["workload"] += 1

        # Workload imbalance across team
        workloads = [s["workload"] for s in self.staff_list]
        workload_imbalance = float(np.std(workloads))

        # Reward = - (resolution_time + lambda * workload_imbalance) + skill_bonus
        skill_bonus = 2.0 if has_skill else -1.0
        reward = - (actual_res_time + self.lambda_penalty * workload_imbalance) + skill_bonus

        # Decay workload occasionally
        for s in self.staff_list:
            if s["workload"] > 0 and random.random() < 0.3:
                s["workload"] -= 1

        next_state = self.sample_state()
        info = {
            "staff_id": staff["id"],
            "staff_name": staff["name"],
            "resolution_time": round(actual_res_time, 2),
            "workload_imbalance": round(workload_imbalance, 2),
            "current_workload": staff["workload"]
        }
        return next_state, reward, info
