import pandas as pd
import numpy as np
from typing import Dict, Any, List

FEATURE_COLUMNS = [
    "severity", "previous_incidents", "lamp_hours",
    "power_indicator_on", "power_indicator_off",
    "remote_no_response", "compressor_no_sound", "cooling_low", "ac_water_leak",
    "projector_no_display", "lamp_led_blinking", "router_led_off",
    "multiple_users_affected", "single_user_affected", "socket_tested_ok",
    "lighting_flicker", "recently_installed", "noise", "vibration",
    "dept_CSE", "dept_ECE", "dept_EEE", "dept_Mechanical", "dept_Biotechnology"
]

def preprocess_ticket_features(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocesses DataFrame of ticket records into numeric feature matrix."""
    processed = pd.DataFrame(index=df.index)

    # Numeric features (preserve NaNs for imputer)
    processed["severity"] = pd.to_numeric(df["severity"], errors="coerce")
    processed["previous_incidents"] = pd.to_numeric(df["previous_incidents"], errors="coerce")
    processed["lamp_hours"] = pd.to_numeric(df["lamp_hours"], errors="coerce")

    # Categorical / boolean encoding
    processed["power_indicator_on"] = (df["power_indicator"] == "on").astype(float)
    processed["power_indicator_off"] = (df["power_indicator"] == "off").astype(float)
    
    bool_cols = [
        "remote_no_response", "compressor_no_sound", "cooling_low", "ac_water_leak",
        "projector_no_display", "multiple_users_affected", "single_user_affected",
        "socket_tested_ok", "lighting_flicker", "recently_installed", "noise", "vibration"
    ]
    for c in bool_cols:
        processed[c] = df[c].astype(float) if c in df.columns else 0.0

    processed["lamp_led_blinking"] = (df["lamp_led"] == "blinking").astype(float) if "lamp_led" in df.columns else 0.0
    processed["router_led_off"] = (df["router_led"] == "off").astype(float) if "router_led" in df.columns else 0.0

    # One-hot encode department
    dept = df["department"] if "department" in df.columns else pd.Series(["General"] * len(df))
    for d in ["CSE", "ECE", "EEE", "Mechanical", "Biotechnology"]:
        processed[f"dept_{d}"] = (dept == d).astype(float)

    # Fill any missing columns with 0.0
    for col in FEATURE_COLUMNS:
        if col not in processed.columns:
            processed[col] = 0.0

    return processed[FEATURE_COLUMNS]

def extract_features_from_dict(ticket_data: Dict[str, Any]) -> pd.DataFrame:
    """Converts a single ticket query dictionary into a 1-row DataFrame."""
    symptoms = ticket_data.get("symptoms", {})
    row = {
        "department": ticket_data.get("department", "CSE"),
        "severity": ticket_data.get("severity", symptoms.get("severity", np.nan)),
        "previous_incidents": ticket_data.get("previous_incidents", symptoms.get("previous_incidents", np.nan)),
        "lamp_hours": symptoms.get("lamp_hours", np.nan),
        "power_indicator": symptoms.get("power_indicator", np.nan),
        "remote_no_response": symptoms.get("remote_no_response", False),
        "compressor_no_sound": symptoms.get("compressor_no_sound", False),
        "cooling_low": symptoms.get("cooling_low", False),
        "ac_water_leak": symptoms.get("ac_water_leak", False),
        "projector_no_display": symptoms.get("projector_no_display", False),
        "lamp_led": symptoms.get("lamp_led", "off"),
        "router_led": symptoms.get("router_led", "on"),
        "multiple_users_affected": symptoms.get("multiple_users_affected", False),
        "single_user_affected": symptoms.get("single_user_affected", False),
        "socket_tested_ok": symptoms.get("socket_tested_ok", False),
        "lighting_flicker": symptoms.get("lighting_flicker", False),
        "recently_installed": symptoms.get("recently_installed", False),
        "noise": symptoms.get("noise", False),
        "vibration": symptoms.get("vibration", False),
    }
    df = pd.DataFrame([row])
    return preprocess_ticket_features(df)
