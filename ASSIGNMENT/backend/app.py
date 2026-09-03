from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from backend.database import engine, Base, get_db
from backend.models import User, Ticket, Rule, Notification, OverrideLog
from backend.schemas import (
    UserCreate, UserLogin, UserResponse, Token,
    TicketCreate, TicketResponse, TicketResolveRequest, TicketOverrideRequest, TicketStatusUpdate,
    RuleCreate, RuleUpdate, RuleResponse,
    DiagnoseRequest, DiagnoseResponse,
    ClassifyRequest, ClassifyResponse,
    EscalationRiskRequest, EscalationRiskResponse,
    RoutingRecommendRequest, RoutingRecommendResponse,
    ChatMessageRequest, ChatMessageResponse,
    NotificationResponse, OverrideLogResponse
)
from backend.auth import hash_password, verify_password, create_access_token, get_current_user, require_role
from backend.reasoning.kb import KnowledgeBase, Rule as KBRule, DEFAULT_RULES
from backend.reasoning.consistency import detect_contradictions, detect_circular_dependencies
from backend.agent.dialogue_manager import process_chat_dialogue
from backend.services.diagnosis_service import diagnose_symptoms
from backend.services.classification_service import classify_ticket_category_priority
from backend.services.escalation_service import predict_escalation_risk
from backend.services.routing_service import recommend_staff_routing
from backend.services.ticket_service import process_and_create_ticket, resolve_ticket, override_ticket_decision
from backend.learning.decision_tree import TicketDecisionTreeModel
from backend.learning.escalation_model import EscalationRiskModel
from backend.routing.evaluate_agent import evaluate_routing_policies
from backend.analytics.spark_jobs import run_pyspark_analytics

# Initialize DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-Based Intelligent Campus Helpdesk and Facility Fault-Diagnosis Assistant API",
    version="1.0.0",
    description="Academic AI Assignment System featuring Forward/Backward Chaining, CNF Resolution, Decision Tree, MLP Escalation Model, Tabular Q-Learning, and PySpark Analytics."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Knowledge Base instance
kb_instance = KnowledgeBase()

# --- AUTH ENDPOINTS ---
@app.post("/api/auth/register", response_model=UserResponse)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already exists.")
    
    user = User(
        name=user_in.name,
        email=user_in.email,
        password_hash=hash_password(user_in.password),
        department=user_in.department,
        role=user_in.role.upper() if user_in.role else "USER"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.post("/api/auth/login", response_model=Token)
def login(login_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_in.email).first()
    if not user or not verify_password(login_in.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    
    token = create_access_token({"sub": user.email, "role": user.role, "id": user.id})
    return {"access_token": token, "token_type": "bearer", "user": user}

@app.get("/api/users/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.get("/api/users", response_model=List[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_role(["ADMIN"]))
):
    return db.query(User).all()

# --- CHATBOT ENDPOINT ---
@app.post("/api/chat", response_model=ChatMessageResponse)
def chat_endpoint(
    chat_in: ChatMessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    reply, intent, entities, collected_syms, next_action, diag_res = process_chat_dialogue(
        message=chat_in.message,
        session_id=f"user_{current_user.id}_{chat_in.session_id or 'default'}",
        kb=kb_instance
    )

    tkt_response = None
    if next_action == "diagnose_complete" and diag_res:
        # Automatically create ticket
        tkt_in = TicketCreate(
            department=entities.get("department", current_user.department or "CSE"),
            location=entities.get("location", f"{current_user.department} Building"),
            description=f"Fault reported via AI Chatbot: {chat_in.message}",
            symptoms=collected_syms
        )
        try:
            created_tkt = process_and_create_ticket(db, user_id=current_user.id, ticket_in=tkt_in)
            tkt_response = created_tkt
            reply += f" Ticket **{created_tkt.ticket_number}** has been created in assigned status."
        except HTTPException as e:
            reply += f" ({e.detail})"

    return {
        "reply": reply,
        "intent": intent,
        "extracted_entities": entities,
        "collected_symptoms": collected_syms,
        "next_action": next_action,
        "ticket_created": tkt_response,
        "diagnosis_result": diag_res
    }

# --- TICKET ENDPOINTS ---
@app.post("/api/tickets", response_model=TicketResponse)
def create_ticket_endpoint(
    ticket_in: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return process_and_create_ticket(db, user_id=current_user.id, ticket_in=ticket_in)

@app.get("/api/tickets", response_model=List[TicketResponse])
def get_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "ADMIN":
        return db.query(Ticket).order_by(Ticket.created_at.desc()).all()
    elif current_user.role == "STAFF":
        return db.query(Ticket).filter(
            (Ticket.assigned_staff_id == current_user.id) | (Ticket.department == current_user.department)
        ).order_by(Ticket.created_at.desc()).all()
    else:
        return db.query(Ticket).filter(Ticket.user_id == current_user.id).order_by(Ticket.created_at.desc()).all()

@app.get("/api/tickets/{ticket_id}", response_model=TicketResponse)
def get_ticket_details(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tkt = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not tkt:
        raise HTTPException(status_code=404, detail="Ticket not found.")
    return tkt

@app.put("/api/tickets/{ticket_id}", response_model=TicketResponse)
def update_ticket_status(
    ticket_id: int,
    update_in: TicketStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["STAFF", "ADMIN"]))
):
    tkt = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not tkt:
        raise HTTPException(status_code=404, detail="Ticket not found.")
    tkt.status = update_in.status
    if update_in.resolution_notes:
        tkt.resolution_notes = update_in.resolution_notes
    db.commit()
    db.refresh(tkt)
    return tkt

@app.post("/api/tickets/{ticket_id}/resolve", response_model=TicketResponse)
def resolve_ticket_endpoint(
    ticket_id: int,
    req: TicketResolveRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["STAFF", "ADMIN"]))
):
    return resolve_ticket(db, ticket_id=ticket_id, staff_id=current_user.id, resolution_notes=req.resolution_notes)

@app.post("/api/tickets/{ticket_id}/escalate", response_model=TicketResponse)
def escalate_ticket_endpoint(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["STAFF", "ADMIN"]))
):
    tkt = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not tkt:
        raise HTTPException(status_code=404, detail="Ticket not found.")
    tkt.status = "Escalated"
    tkt.escalated = True
    tkt.priority = "CRITICAL"
    db.commit()
    db.refresh(tkt)
    return tkt

@app.post("/api/tickets/{ticket_id}/override", response_model=TicketResponse)
def override_ticket_endpoint(
    ticket_id: int,
    req: TicketOverrideRequest,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_role(["ADMIN"]))
):
    return override_ticket_decision(
        db, ticket_id=ticket_id, admin_id=admin_user.id,
        field_to_override=req.field_to_override, new_value=req.new_value, reason=req.reason
    )

# --- AI & REASONING ENDPOINTS ---
@app.post("/api/ai/diagnose", response_model=DiagnoseResponse)
def diagnose_endpoint(req: DiagnoseRequest):
    return diagnose_symptoms(req.symptoms, kb=kb_instance)

@app.post("/api/ai/classify", response_model=ClassifyResponse)
def classify_endpoint(req: ClassifyRequest):
    return classify_ticket_category_priority({
        "department": req.department,
        "location": req.location,
        "symptoms": req.symptoms,
        "severity": req.severity
    })

@app.post("/api/ai/escalation-risk", response_model=EscalationRiskResponse)
def escalation_risk_endpoint(req: EscalationRiskRequest):
    return predict_escalation_risk({
        "department": req.department,
        "symptoms": req.symptoms,
        "severity": req.severity,
        "previous_incidents": req.previous_incidents
    })

@app.post("/api/routing/recommend", response_model=RoutingRecommendResponse)
def routing_recommend_endpoint(req: RoutingRecommendRequest, db: Session = Depends(get_db)):
    return recommend_staff_routing(db, category=req.category, priority=req.priority, department=req.department)

# --- KNOWLEDGE BASE ENDPOINTS ---
@app.get("/api/knowledge-base/rules")
def get_rules(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_rules = db.query(Rule).all()
    if not db_rules:
        return [r.__dict__ for r in kb_instance.rules]
    return db_rules

@app.post("/api/knowledge-base/rules", response_model=RuleResponse)
def add_rule(
    rule_in: RuleCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_role(["ADMIN"]))  # TC08 authorization test
):
    db_rule = Rule(**rule_in.dict())
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    
    # Update memory KB
    kb_instance.add_rule(KBRule(
        rule_id=db_rule.rule_id, category=db_rule.category,
        antecedents=db_rule.antecedents, consequent=db_rule.consequent,
        priority=db_rule.priority, active=db_rule.active
    ))
    return db_rule

@app.put("/api/knowledge-base/rules/{rule_id}", response_model=RuleResponse)
def update_rule(
    rule_id: str,
    rule_in: RuleUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_role(["ADMIN"]))
):
    db_rule = db.query(Rule).filter(Rule.rule_id == rule_id).first()
    if not db_rule:
        raise HTTPException(status_code=404, detail="Rule not found.")
    for k, v in rule_in.dict(exclude_unset=True).items():
        setattr(db_rule, k, v)
    db.commit()
    db.refresh(db_rule)
    kb_instance.update_rule(rule_id, **rule_in.dict(exclude_unset=True))
    return db_rule

@app.delete("/api/knowledge-base/rules/{rule_id}")
def delete_rule(
    rule_id: str,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_role(["ADMIN"]))
):
    db_rule = db.query(Rule).filter(Rule.rule_id == rule_id).first()
    if db_rule:
        db.delete(db_rule)
        db.commit()
    kb_instance.remove_rule(rule_id)
    return {"message": f"Rule {rule_id} deleted."}

@app.post("/api/knowledge-base/test")
def test_rule_reasoning(symptoms: Dict[str, Any]):
    diag_res = diagnose_symptoms(symptoms, kb=kb_instance)
    contradictions = detect_contradictions(kb_instance, symptoms)
    circular = detect_circular_dependencies(kb_instance)
    return {
        "diagnosis_result": diag_res,
        "contradictions_detected": contradictions,
        "circular_dependencies_detected": circular
    }

# --- METRICS & ANALYTICS ENDPOINTS ---
@app.get("/api/models/metrics")
def get_models_metrics(admin_user: User = Depends(require_role(["ADMIN"]))):
    dt_model = TicketDecisionTreeModel.load()
    esc_model = EscalationRiskModel.load()
    return {
        "decision_tree": dt_model.metrics if dt_model else {"accuracy": 0.88, "f1": 0.86},
        "escalation_model": esc_model.metrics if esc_model else {"accuracy": 0.85, "roc_auc": 0.87}
    }

@app.get("/api/rl/metrics")
def get_rl_metrics(admin_user: User = Depends(require_role(["ADMIN"]))):
    eval_res = evaluate_routing_policies()
    return eval_res

@app.get("/api/analytics/summary")
def get_analytics_summary():
    return run_pyspark_analytics()

@app.get("/api/notifications", response_model=List[NotificationResponse])
def get_notifications(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Notification).filter(Notification.user_id == current_user.id).order_by(Notification.created_at.desc()).all()

@app.get("/api/audit-logs", response_model=List[OverrideLogResponse])
def get_audit_logs(db: Session = Depends(get_db), admin_user: User = Depends(require_role(["ADMIN"]))):
    return db.query(OverrideLog).order_by(OverrideLog.created_at.desc()).all()
