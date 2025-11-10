from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, Request
from sqlalchemy.orm import Session
from app.schemas.email import EmailCreate, EmailRead
from app.db.session import get_session
from app.db.models import Notification
from app.services.email_service import send_email
from app.depends.auth_dep import get_current_user
from app.utils.logger import logger
from app.rate_limiter import limiter

router = APIRouter(prefix="/email", tags=["email"])


@router.post("/send-email", response_model=EmailRead)
@limiter.limit("5/minute")
def create_email(
    request: Request,
    email: EmailCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    try:
        logger.info(
            f"Email send request by user_id={current_user.id} to={email.to_email}"
        )

        notif = Notification(
            user_id=current_user.id,
            to_email=email.to_email,
            subject=email.subject,
            body=email.body,
            status="queued",
        )
        db.add(notif)
        db.commit()
        db.refresh(notif)

        background_tasks.add_task(send_email, notif.id, db)

        logger.info(f"Queued email id={notif.id} for background sending")
        return notif

    except Exception as e:
        logger.error(f"Failed to queue email for {email.to_email}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
