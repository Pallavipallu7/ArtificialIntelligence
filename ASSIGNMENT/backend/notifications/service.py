from sqlalchemy.orm import Session
from backend.models import Notification

def create_notification(db: Session, user_id: int, ticket_id: int, message: str, notification_type: str = "STATUS_UPDATE") -> Notification:
    notif = Notification(
        user_id=user_id,
        ticket_id=ticket_id,
        message=message,
        notification_type=notification_type,
        is_read=False
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif

def get_user_notifications(db: Session, user_id: int):
    return db.query(Notification).filter(Notification.user_id == user_id).order_by(Notification.created_at.desc()).all()
