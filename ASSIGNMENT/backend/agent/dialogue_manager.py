from typing import Dict, Any, Tuple, List, Optional
from backend.agent.intent_classifier import classify_intent
from backend.agent.entity_extractor import extract_entities
from backend.reasoning.kb import KnowledgeBase
from backend.reasoning.forward_chaining import forward_chain
from backend.reasoning.backward_chaining import backward_chain

# Session state cache in memory
SESSION_STATES: Dict[str, Dict[str, Any]] = {}

def get_or_create_session(session_id: str) -> Dict[str, Any]:
    if session_id not in SESSION_STATES:
        SESSION_STATES[session_id] = {
            "symptoms": {},
            "department": "CSE",
            "location": "CSE Lab 2",
            "description": "",
            "pending_question": None,
            "asked_facts": []
        }
    return SESSION_STATES[session_id]

def reset_session(session_id: str):
    if session_id in SESSION_STATES:
        del SESSION_STATES[session_id]

def process_chat_dialogue(
    message: str,
    session_id: str = "default",
    kb: Optional[KnowledgeBase] = None
) -> Tuple[str, str, Dict[str, Any], Dict[str, Any], str, Optional[Dict[str, Any]]]:
    """
    Main dialogue processing function.
    Returns: (reply, intent, extracted_entities, collected_symptoms, next_action, diagnosis_dict)
    """
    if kb is None:
        kb = KnowledgeBase()

    session = get_or_create_session(session_id)
    in_dialogue_state = session["pending_question"] is not None or len(session["symptoms"]) > 0

    intent = classify_intent(message, in_dialogue_state=in_dialogue_state)
    entities = extract_entities(message)

    # 1. Update session entity & symptom memory
    if entities.get("department"):
        session["department"] = entities["department"]
    if entities.get("location"):
        session["location"] = entities["location"]
    
    extracted_syms = entities.get("symptoms", {})
    if extracted_syms:
        session["symptoms"].update(extracted_syms)

    # If replying to a pending question
    if session["pending_question"] and intent in ["provide_symptom", "report_fault", "unknown"]:
        target_fact = session["pending_question"]
        val_text = message.strip().lower()
        if "yes" in val_text or "on" in val_text or "blinking" in val_text:
            session["symptoms"][target_fact] = True if "blinking" not in val_text else "blinking"
        elif "no" in val_text or "off" in val_text or "silent" in val_text:
            session["symptoms"][target_fact] = False if "off" not in val_text else "off"
        elif val_text.isdigit():
            session["symptoms"][target_fact] = int(val_text)
        else:
            session["symptoms"][target_fact] = val_text
        session["pending_question"] = None

    # Handle Intent Switch
    if intent == "unknown":
        reply = "I am the Intelligent Campus Helpdesk Assistant. I can assist you with reporting facility faults (AC, Projector, Wi-Fi, Lighting, Equipment), checking ticket status, or clarifying symptoms. How can I help you today?"
        return reply, intent, entities, session["symptoms"], "general", None

    elif intent == "ask_help":
        reply = "I can help you diagnose and report campus infrastructure problems like AC cooling issues, projector lamp failures, Wi-Fi connectivity drops, or lab equipment faults. Simply tell me what problem you are facing!"
        return reply, intent, entities, session["symptoms"], "general", None

    elif intent == "check_status":
        tkt_num = entities.get("ticket_number")
        if tkt_num:
            reply = f"Looking up ticket {tkt_num}... Please check the ticket details in 'My Tickets' or ticket details page."
            return reply, intent, entities, session["symptoms"], "status_info", None
        else:
            reply = "You can view the current status of all your complaints under the 'My Tickets' tab or enter a ticket number like 'TKT-1001'."
            return reply, intent, entities, session["symptoms"], "status_info", None

    # 2. Run Forward Chaining Diagnosis
    diagnosis, confidence, proof_trace, _ = forward_chain(kb, session["symptoms"])

    if diagnosis:
        # Diagnosis successful!
        diag_dict = {
            "diagnosis": diagnosis,
            "confidence": confidence,
            "proof_trace": proof_trace,
            "symptoms": session["symptoms"]
        }
        reply = f"Based on the reported symptoms, the probable cause is: **{diagnosis}** (Confidence: {int(confidence*100)}%). I will now automatically classify, predict escalation risk, and route your ticket to maintenance staff."
        reset_session(session_id)
        return reply, "report_fault", entities, diag_dict["symptoms"], "diagnose_complete", diag_dict

    # 3. If diagnosis not complete, use Backward Chaining to ask clarifying questions
    missing_facts, questions, candidates = backward_chain(kb, session["symptoms"])

    # Pick first unasked missing fact
    next_fact = None
    next_question = None
    for mf, q in zip(missing_facts, questions):
        if mf not in session["asked_facts"] and mf not in session["symptoms"]:
            next_fact = mf
            next_question = q
            break

    if next_question and next_fact:
        session["pending_question"] = next_fact
        session["asked_facts"].append(next_fact)
        reply = f"I can help report this issue. {next_question}"
        return reply, "report_fault", entities, session["symptoms"], "ask_clarification", None
    else:
        # Fallback if no specific question can be derived
        reply = "Thank you for the information. I have recorded your report and will proceed with ticket creation."
        reset_session(session_id)
        return reply, "report_fault", entities, session["symptoms"], "diagnose_complete", {
            "diagnosis": "General Facility Fault",
            "confidence": 0.75,
            "proof_trace": [],
            "symptoms": session["symptoms"]
        }
