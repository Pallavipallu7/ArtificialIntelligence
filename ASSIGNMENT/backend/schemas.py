from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# --- Auth & User ---
class UserBase(BaseModel):
    name: str
    email: str
    department: str
    role: Optional[str] = "USER"

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# --- Knowledge Base Rule ---
class RuleBase(BaseModel):
    rule_id: str
    category: str
    antecedents: Dict[str, Any]
    consequent: str
    priority: Optional[int] = 1
    active: Optional[bool] = True

class RuleCreate(RuleBase):
    pass

class RuleUpdate(BaseModel):
    category: Optional[str] = None
    antecedents: Optional[Dict[str, Any]] = None
    consequent: Optional[str] = None
    priority: Optional[int] = None
    active: Optional[bool] = None

class RuleResponse(RuleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Ticket ---
class TicketCreate(BaseModel):
    department: str
    location: str
    description: str
    symptoms: Optional[Dict[str, Any]] = {}

class TicketStatusUpdate(BaseModel):
    status: str
    resolution_notes: Optional[str] = None

class TicketResolveRequest(BaseModel):
    resolution_notes: str

class TicketOverrideRequest(BaseModel):
    field_to_override: str  # "assigned_staff_id", "category", "priority", "status"
    new_value: str
    reason: str

class TicketResponse(BaseModel):
    id: int
    ticket_number: str
    user_id: int
    department: str
    location: str
    description: str
    symptoms: Optional[Dict[str, Any]] = {}
    category: Optional[str] = None
    priority: Optional[str] = "MEDIUM"
    diagnosed_cause: Optional[str] = None
    diagnosis_confidence: Optional[float] = 0.0
    escalation_probability: Optional[float] = 0.0
    escalated: bool = False
    assigned_staff_id: Optional[int] = None
    status: str
    ai_explanation: Optional[Dict[str, Any]] = {}
    created_at: datetime
    diagnosed_at: Optional[datetime] = None
    assigned_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None

    class Config:
        from_attributes = True

# --- AI & Reasoning ---
class DiagnoseRequest(BaseModel):
    symptoms: Dict[str, Any]
    department: Optional[str] = "General"

class ProofTraceStep(BaseModel):
    step: int
    matched_rule: str
    antecedents: Dict[str, Any]
    derived_fact: str
    confidence: float

class DiagnoseResponse(BaseModel):
    diagnosis: Optional[str]
    confidence: float
    reasoning_method: str
    proof_trace: List[Dict[str, Any]]
    missing_symptoms: List[str]
    cached: bool = False
    cnf_clause: Optional[str] = None
    resolution_steps: Optional[List[str]] = []

class ClassifyRequest(BaseModel):
    department: str
    location: str
    symptoms: Dict[str, Any]
    severity: Optional[int] = 3

class ClassifyResponse(BaseModel):
    category: str
    priority: str
    confidence: float

class EscalationRiskRequest(BaseModel):
    department: str
    symptoms: Dict[str, Any]
    severity: Optional[int] = 3
    previous_incidents: Optional[int] = 0

class EscalationRiskResponse(BaseModel):
    escalation_probability: float
    risk_level: str
    missing_values_handled: bool

class RoutingRecommendRequest(BaseModel):
    category: str
    priority: str
    department: str

class StaffRecommendItem(BaseModel):
    staff_id: int
    name: str
    department: str
    current_workload: int
    predicted_utility: float

class RoutingRecommendResponse(BaseModel):
    recommended_staff_id: int
    recommended_staff_name: str
    predicted_utility: float
    reason: str
    candidates: List[StaffRecommendItem]

# --- Chatbot ---
class ChatMessageRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"
    current_symptoms: Optional[Dict[str, Any]] = {}
    ticket_context_id: Optional[str] = None

class ChatMessageResponse(BaseModel):
    reply: str
    intent: str
    extracted_entities: Dict[str, Any]
    collected_symptoms: Dict[str, Any]
    next_action: str  # "ask_clarification", "diagnose_complete", "ticket_created", "status_info", "general"
    ticket_created: Optional[TicketResponse] = None
    diagnosis_result: Optional[DiagnoseResponse] = None

# --- Notification & Override ---
class NotificationResponse(BaseModel):
    id: int
    user_id: int
    ticket_id: Optional[int]
    message: str
    notification_type: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

class OverrideLogResponse(BaseModel):
    id: int
    ticket_id: int
    admin_id: int
    old_value: str
    new_value: str
    reason: str
    created_at: datetime

    class Config:
        from_attributes = True
