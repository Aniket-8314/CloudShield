from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import get_current_user
from app.core.database import get_db
from app.models.audit import AuditLog
from app.models.user import User


router = APIRouter(prefix="/audit", tags=["Audit"])


def require_admin(current_user: User):

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    return current_user


@router.get("/logs")
def get_logs(current_user: User = Depends(get_current_user), db=Depends(get_db)):

    require_admin(current_user)

    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(50).all()

    return [
        {
            "user_id": log.user_id,
            "resource": log.resource,
            "action": log.action,
            "decision": log.decision,
            "reason": log.reason,
            "timestamp": log.timestamp,
        }
        for log in logs
    ]


@router.get("/debug/count")
def debug_count(current_user: User = Depends(get_current_user), db=Depends(get_db)):

    count = db.query(AuditLog).count()

    return {"audit_log_count": count}
