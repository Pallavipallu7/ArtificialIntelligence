import pandas as pd
import numpy as np
import random
from pathlib import Path
from backend.config import DATA_DIR

DEPARTMENTS = ["CSE", "ECE", "EEE", "Mechanical", "Biotechnology"]
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

def generate_synthetic_dataset(num_samples: int = 120, file_path: Path = None) -> pd.DataFrame:
    if file_path is None:
        file_path = DATA_DIR / "historical_tickets.csv"

    np.random.seed(42)
    random.seed(42)

    rows = []
    for i in range(1, num_samples + 1):
        dept = random.choice(DEPARTMENTS)
        cat = random.choice(CATEGORIES)
        loc = f"{dept} Building - Room {random.randint(101, 410)}"
        
        power_ind = random.choice(["on", "off", "on"])
        remote_resp = random.choice([True, False])
        comp_silent = random.choice([True, False])
        cooling_low = random.choice([True, False])
        ac_leak = random.choice([True, False])
        proj_no_disp = random.choice([True, False])
        lamp_led = random.choice(["off", "on", "blinking"])
        lamp_hrs = float(random.randint(500, 4500))
        router_led = random.choice(["on", "off"])
        mult_users = random.choice([True, False])
        sing_user = random.choice([True, False])
        socket_ok = random.choice([True, False])
        light_flicker = random.choice([True, False])
        rec_inst = random.choice([True, False])
        noise = random.choice([True, False])
        vibration = random.choice([True, False])
        
        severity = random.randint(1, 5)
        prev_incidents = random.randint(0, 8)
        
        # Priority heuristics based on category & severity
        if severity >= 4 or cat in ["AC_POWER", "PROJECTOR_LAMP", "CLASSROOM_POWER", "LAB_EQUIPMENT_INTERNAL"]:
            priority = random.choice(["HIGH", "CRITICAL"])
        elif severity == 3:
            priority = random.choice(["MEDIUM", "HIGH"])
        else:
            priority = random.choice(["LOW", "MEDIUM"])

        # Escalation rules synthetic logic: high severity, previous incidents, internal equipment faults -> higher escalation prob
        esc_prob = 0.1
        if priority in ["HIGH", "CRITICAL"]:
            esc_prob += 0.35
        if prev_incidents >= 4:
            esc_prob += 0.30
        if cat in ["LAB_EQUIPMENT_INTERNAL", "EQUIPMENT_OVERHEATING"]:
            esc_prob += 0.20
            
        escalated = 1 if (random.random() < esc_prob) else 0
        resolution_time = float(random.randint(2, 48) + (escalated * random.randint(10, 36)))
        assigned_staff = random.randint(1, 6)

        row = {
            "ticket_number": f"TKT-{1000 + i}",
            "department": dept,
            "location": loc,
            "category": cat,
            "priority": priority,
            "power_indicator": power_ind,
            "remote_no_response": remote_resp,
            "compressor_no_sound": comp_silent,
            "cooling_low": cooling_low,
            "ac_water_leak": ac_leak,
            "projector_no_display": proj_no_disp,
            "lamp_led": lamp_led,
            "lamp_hours": lamp_hrs,
            "router_led": router_led,
            "multiple_users_affected": mult_users,
            "single_user_affected": sing_user,
            "socket_tested_ok": socket_ok,
            "lighting_flicker": light_flicker,
            "recently_installed": rec_inst,
            "noise": noise,
            "vibration": vibration,
            "severity": severity,
            "previous_incidents": prev_incidents,
            "resolution_time": resolution_time,
            "escalated": escalated,
            "assigned_staff": assigned_staff
        }
        rows.append(row)

    df = pd.DataFrame(rows)

    # Deliberately introduce missing values (NaN) in ~15% of records for missing-data handling demo (TC05)
    for col in ["lamp_hours", "severity", "previous_incidents", "router_led", "power_indicator"]:
        mask = np.random.rand(len(df)) < 0.15
        df.loc[mask, col] = np.nan

    df.to_csv(file_path, index=False)
    print(f"Synthetic dataset with {len(df)} records saved to {file_path}")
    return df

if __name__ == "__main__":
    generate_synthetic_dataset()
