import smtplib
from email.mime.text import MIMEText
from app.core.config import settings
from app.db.models import Notification
from sqlalchemy.orm import Session


def send_email(notification_id: int, db: Session):
    # Get notification from DB
    notif = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notif:
        return

    try:
        # Prepare message
        msg = MIMEText(notif.body)
        msg["Subject"] = notif.subject
        msg["From"] = settings.SMTP_EMAIL
        msg["To"] = notif.to_email

        # Connect to Gmail SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(settings.SMTP_EMAIL, settings.SMTP_PASSWORD)
            server.send_message(msg)

        notif.status = "sent"
    except Exception as e:
        notif.status = "failed"
        notif.error_message = str(e)
    finally:
        db.add(notif)
        db.commit()
