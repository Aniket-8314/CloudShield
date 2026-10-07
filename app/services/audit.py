from app.models.audit import AuditLog


def create_audit_log(
    db, user_id: int, resource: str, action: str, decision: str, reason: str
):
    log = AuditLog(
        user_id=user_id,
        resource=resource,
        action=action,
        decision=decision,
        reason=reason,
    )

    db.add(log)
    db.commit()
