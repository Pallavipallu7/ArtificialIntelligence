from backend.database import SessionLocal, engine, Base
from backend.models import User, Rule, Ticket, Notification
from backend.auth import hash_password
from backend.reasoning.kb import DEFAULT_RULES
from backend.services.ticket_service import process_and_create_ticket
from backend.schemas import TicketCreate

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    print("Seeding Users...")
    users_data = [
        {"name": "System Administrator", "email": "admin@campus.edu", "password": "admin123", "department": "IT", "role": "ADMIN"},
        {"name": "Arun Kumar", "email": "staff1@campus.edu", "password": "staff123", "department": "CSE", "role": "STAFF"},
        {"name": "Priya Sharma", "email": "staff2@campus.edu", "password": "staff123", "department": "ECE", "role": "STAFF"},
        {"name": "Rajesh Verma", "email": "staff3@campus.edu", "password": "staff123", "department": "EEE", "role": "STAFF"},
        {"name": "Sneha Patel", "email": "staff4@campus.edu", "password": "staff123", "department": "Mechanical", "role": "STAFF"},
        {"name": "Vikram Singh", "email": "staff5@campus.edu", "password": "staff123", "department": "Biotechnology", "role": "STAFF"},
        {"name": "Ananya Reddy", "email": "staff6@campus.edu", "password": "staff123", "department": "IT", "role": "STAFF"},
        {"name": "Rahul Student", "email": "student@campus.edu", "password": "student123", "department": "CSE", "role": "USER"},
        {"name": "Anita Student", "email": "student2@campus.edu", "password": "student123", "department": "ECE", "role": "USER"},
        {"name": "Karan Student", "email": "student3@campus.edu", "password": "student123", "department": "EEE", "role": "USER"}
    ]

    user_map = {}
    for u in users_data:
        existing = db.query(User).filter(User.email == u["email"]).first()
        if not existing:
            new_user = User(
                name=u["name"],
                email=u["email"],
                password_hash=hash_password(u["password"]),
                department=u["department"],
                role=u["role"]
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            user_map[u["email"]] = new_user
        else:
            user_map[u["email"]] = existing

    print("Seeding Knowledge Base Rules (R1 - R12)...")
    for r in DEFAULT_RULES:
        existing_rule = db.query(Rule).filter(Rule.rule_id == r["rule_id"]).first()
        if not existing_rule:
            db_rule = Rule(
                rule_id=r["rule_id"],
                category=r["category"],
                antecedents=r["antecedents"],
                consequent=r["consequent"],
                priority=r["priority"],
                active=r["active"]
            )
            db.add(db_rule)
    db.commit()

    print("Seeding Demonstration Tickets...")
    student_user = user_map.get("student@campus.edu")
    if student_user:
        demos = [
            {
                "department": "CSE",
                "location": "CSE Lab 2",
                "description": "AC power is completely off and remote doesn't respond.",
                "symptoms": {"power_indicator": "off", "remote_no_response": True}
            },
            {
                "department": "CSE",
                "location": "CSE Seminar Hall",
                "description": "AC power is ON but compressor makes no sound and cooling is very low.",
                "symptoms": {"power_indicator": "on", "compressor_no_sound": True, "cooling_low": True}
            },
            {
                "department": "ECE",
                "location": "ECE Lab 1",
                "description": "Wi-Fi is down and router LED is OFF.",
                "symptoms": {"wifi_no_connectivity": True, "router_led": "off"}
            },
            {
                "department": "Mechanical",
                "location": "Mech Design Studio",
                "description": "Projector displays no image and lamp LED is blinking.",
                "symptoms": {"projector_no_display": True, "lamp_led": "blinking"}
            }
        ]

        for d in demos:
            existing_tkt = db.query(Ticket).filter(Ticket.description == d["description"]).first()
            if not existing_tkt:
                try:
                    process_and_create_ticket(db, user_id=student_user.id, ticket_in=TicketCreate(**d))
                except Exception as e:
                    print(f"Demo ticket seed notice: {e}")

    db.close()
    print("Database seeding completed successfully!")

if __name__ == "__main__":
    seed_database()
