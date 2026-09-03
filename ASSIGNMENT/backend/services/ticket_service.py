import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from backend.models import Ticket, User, OverrideLog
from backend.schemas import TicketCreate
from backend.services.diagnosis_service import diagnose_symptoms
from backend.services.classification_service import classify_ticket_category_priority
from backend.services.escalation_service import predict_escalation_risk
from backend.services.routing_service import recommend_staff_routing
from backend.notifications.service import create_notification

def process_and_create_ticket(
    db: Session,
    user_id: int,
    ticket_in: TicketCreate
) -> Ticket:
    # STEP 1: Validate input
    if not ticket_in.description or len(ticket_in.description.strip()) < 5:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Ticket description is incomplete or too short."
        )

    # STEP 2: Check duplicate reports (TC09 compliance)
    recent_dup = db.query(Ticket).filter(
        Ticket.user_id == user_id,
        Ticket.location == ticket_in.location,
        Ticket.description == ticket_in.description,
        Ticket.status.in_(["Reported", "Diagnosed", "Assigned"])
    ).first()

    if recent_dup:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Duplicate ticket report detected! Active ticket {recent_dup.ticket_number} already exists for this issue."
        )

    # Generate ticket number
    tkt_num = f"TKT-{uuid.uuid4().hex[:6].upper()}"

    # STEP 3: Create ticket record in 'Reported' status
    ticket = Ticket(
        ticket_number=tkt_num,
        user_id=user_id,
        department=ticket_in.department,
        location=ticket_in.location,
        description=ticket_in.description,
        symptoms=ticket_in.symptoms or {},
        status="Reported"
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    # STEP 4 & 5: Run Knowledge-Based Reasoning Engine
    diag_res = diagnose_symptoms(ticket.symptoms)
    
    ticket.diagnosed_cause = diag_res.get("diagnosis") or "General Fault"
    ticket.diagnosis_confidence = diag_res.get("confidence", 0.75)
    ticket.ai_explanation = diag_res.get("explanation", {})
    ticket.diagnosed_at = datetime.utcnow()
    ticket.status = "Diagnosed"

    # STEP 8: Decision Tree Classification
    clf_res = classify_ticket_category_priority({
        "department": ticket.department,
        "location": ticket.location,
        "symptoms": ticket.symptoms
    })
    ticket.category = clf_res["category"]
    ticket.priority = clf_res["priority"]

    # STEP 9: Escalation Risk Prediction
    esc_res = predict_escalation_risk({
        "department": ticket.department,
        "symptoms": ticket.symptoms,
        "severity": ticket.symptoms.get("severity", 3)
    })
    ticket.escalation_probability = esc_res["escalation_probability"]
    ticket.escalated = esc_res["is_high_risk"]

    # STEP 10 & 11: Q-Learning Routing Agent
    routing_res = recommend_staff_routing(
        db=db,
        category=ticket.category,
        priority=ticket.priority,
        department=ticket.department
    )
    ticket.assigned_staff_id = routing_res["recommended_staff_id"]
    ticket.assigned_at = datetime.utcnow()

    # Priority / High Risk Escalation handling (TC06 compliance)
    if ticket.escalated:
        ticket.status = "Escalated"
        ticket.priority = "CRITICAL"
    else:
        ticket.status = "Assigned"

    db.commit()
    db.refresh(ticket)

    # STEP 12: Notify User & Assigned Staff
    create_notification(
        db, user_id=ticket.user_id, ticket_id=ticket.id,
        message=f"Your ticket {ticket.ticket_number} has been created and assigned to staff (Cause: {ticket.diagnosed_cause})."
    )

    if ticket.assigned_staff_id:
        create_notification(
            db, user_id=ticket.assigned_staff_id, ticket_id=ticket.id,
            message=f"New ticket {ticket.ticket_number} assigned to you: {ticket.description[:40]}..."
        )

    return ticket

def resolve_ticket(db: Session, ticket_id: int, staff_id: int, resolution_notes: str) -> Ticket:
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found.")

    ticket.status = "Resolved"
    ticket.resolution_notes = resolution_notes
    ticket.resolved_at = datetime.utcnow()

    db.commit()
    db.refresh(ticket)

    create_notification(
        db, user_id=ticket.user_id, ticket_id=ticket.id,
        message=f"Ticket {ticket.ticket_number} has been RESOLVED by staff: {resolution_notes}"
    )
    return ticket

def override_ticket_decision(db: Session, ticket_id: int, admin_id: int, field_to_override: str, new_value: str, reason: str) -> Ticket:
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found.")

    old_val = str(getattr(ticket, field_to_override, "N/A"))

    if field_to_override == "assigned_staff_id":
        ticket.assigned_staff_id = int(new_value)
    elif hasattr(ticket, field_to_override):
        setattr(ticket, field_to_override, new_value)

    # Create audit log entry
    override_log = OverrideLog(
        ticket_id=ticket.id,
        admin_id=admin_id,
        old_value=old_val,
        new_value=new_value,
        reason=reason
    )
    db.add(override_log)
    db.commit()
    db.refresh(ticket)
    return ticket
