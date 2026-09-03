from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    department = Column(String(50), nullable=False)
    role = Column(String(20), nullable=False, default="USER")  # USER, STAFF, ADMIN
    created_at = Column(DateTime, default=datetime.utcnow)

    tickets = relationship("Ticket", foreign_keys="Ticket.user_id", back_populates="user")
    assigned_tickets = relationship("Ticket", foreign_keys="Ticket.assigned_staff_id", back_populates="assigned_staff")

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String(30), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    department = Column(String(50), nullable=False)
    location = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    symptoms = Column(JSON, nullable=True, default={})
    category = Column(String(50), nullable=True)
    priority = Column(String(20), nullable=True, default="MEDIUM")  # LOW, MEDIUM, HIGH, CRITICAL
    diagnosed_cause = Column(String(100), nullable=True)
    diagnosis_confidence = Column(Float, nullable=True, default=0.0)
    escalation_probability = Column(Float, nullable=True, default=0.0)
    escalated = Column(Boolean, default=False)
    assigned_staff_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String(20), default="Reported")  # Reported, Diagnosed, Assigned, Resolved, Escalated
    ai_explanation = Column(JSON, nullable=True, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    diagnosed_at = Column(DateTime, nullable=True)
    assigned_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    resolution_notes = Column(Text, nullable=True)

    user = relationship("User", foreign_keys=[user_id], back_populates="tickets")
    assigned_staff = relationship("User", foreign_keys=[assigned_staff_id], back_populates="assigned_tickets")

class Rule(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, index=True)
    rule_id = Column(String(20), unique=True, index=True, nullable=False)
    category = Column(String(50), nullable=False)
    antecedents = Column(JSON, nullable=False)  # e.g., {"power_indicator": "off", "remote_no_response": True}
    consequent = Column(String(100), nullable=False)  # e.g., "Power supply failure"
    priority = Column(Integer, default=1)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class RoutingHistory(Base):
    __tablename__ = "routing_histories"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    state = Column(String(100), nullable=False)
    action = Column(Integer, nullable=False)
    reward = Column(Float, nullable=False)
    staff_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=True)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), default="STATUS_UPDATE")
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class OverrideLog(Base):
    __tablename__ = "override_logs"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    old_value = Column(String(100), nullable=False)
    new_value = Column(String(100), nullable=False)
    reason = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
