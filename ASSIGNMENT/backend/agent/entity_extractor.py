import re
from typing import Dict, Any, Optional

DEPARTMENTS = ["CSE", "ECE", "EEE", "Mechanical", "Biotechnology"]

def extract_entities(message: str) -> Dict[str, Any]:
    text = message.lower()
    entities = {}

    # Ticket number extraction
    tkt_match = re.search(r"tkt-\d+", message, re.IGNORECASE)
    if tkt_match:
        entities["ticket_number"] = tkt_match.group(0).upper()

    # Department extraction
    for dept in DEPARTMENTS:
        if dept.lower() in text:
            entities["department"] = dept
            break
    if "department" not in entities:
        entities["department"] = "CSE"

    # Location extraction (e.g. lab 2, room 301, classroom 4)
    loc_match = re.search(r"(lab\s*\d+|room\s*\d+|hall\s*\d+|classroom\s*\d+)", text)
    if loc_match:
        entities["location"] = f"{entities['department']} {loc_match.group(0).title()}"
    else:
        entities["location"] = f"{entities['department']} Building"

    # Extract explicit symptom signals
    symptoms = {}

    # AC symptoms
    if "power indicator" in text or "power led" in text:
        if "off" in text or "not working" in text or "no" in text:
            symptoms["power_indicator"] = "off"
        elif "on" in text or "yes" in text:
            symptoms["power_indicator"] = "on"

    if "remote" in text:
        if "no" in text or "not respond" in text or "dead" in text or "off" in text:
            symptoms["remote_no_response"] = True
        elif "yes" in text or "working" in text:
            symptoms["remote_no_response"] = False

    if "compressor" in text:
        if "silent" in text or "no sound" in text or "no" in text or "stopped" in text:
            symptoms["compressor_no_sound"] = True
        elif "sound" in text or "yes" in text:
            symptoms["compressor_no_sound"] = False

    if "cooling" in text:
        if "low" in text or "not cooling" in text or "poor" in text or "no" in text or "yes" in text:
            symptoms["cooling_low"] = True

    if "water" in text or "leak" in text or "dripping" in text:
        symptoms["ac_water_leak"] = True

    # Projector symptoms
    if "projector" in text or "display" in text or "screen" in text:
        if "no display" in text or "black" in text or "not showing" in text:
            symptoms["projector_no_display"] = True
        if "dim" in text or "faint" in text:
            symptoms["projector_image_dim"] = True

    if "lamp" in text or "led" in text:
        if "blinking" in text or "blink" in text:
            symptoms["lamp_led"] = "blinking"
        elif "off" in text:
            symptoms["power_led"] = "off"

    # Wi-Fi / Router symptoms
    if "wifi" in text or "wi-fi" in text or "internet" in text:
        if "no" in text or "cannot connect" in text or "down" in text:
            symptoms["wifi_no_connectivity"] = True
        if "slow" in text or "intermittent" in text or "drops" in text:
            symptoms["wifi_intermittent"] = True

    if "router" in text:
        if "off" in text:
            symptoms["router_led"] = "off"
        elif "on" in text:
            symptoms["router_led"] = "on"

    if "multiple" in text or "everyone" in text or "all students" in text:
        symptoms["multiple_users_affected"] = True
    elif "single" in text or "only me" in text or "my device" in text:
        symptoms["single_user_affected"] = True

    # Equipment / Lighting symptoms
    if "socket" in text:
        if "ok" in text or "working" in text or "tested" in text or "yes" in text:
            symptoms["socket_tested_ok"] = True

    if "flicker" in text or "flickering" in text:
        symptoms["lighting_flicker"] = True

    if "recent" in text or "new" in text:
        symptoms["recently_installed"] = True

    if "noisy" in text or "noise" in text:
        symptoms["classroom_ac_noisy"] = True
        symptoms["noise"] = True

    if "vibration" in text or "vibrating" in text:
        symptoms["vibration_present"] = True

    entities["symptoms"] = symptoms
    return entities
