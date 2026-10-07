from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.services.policy_engine import check_policy
from app.services.rate_limiter import check_rate_limit
from app.services.proxy import forward_request
from app.services.audit import create_audit_log


router = APIRouter(prefix="/gateway", tags=["Gateway"])


@router.get("/internal/data")
async def gateway_internal_data(
    current_user: User = Depends(get_current_user), db=Depends(get_db)
):

    # 1. Rate limiting
    check_rate_limit(current_user.id)

    # 2. Policy check
    allowed = check_policy(db, current_user, "/internal/data", "GET")

    # 3. DENY
    if not allowed:

        create_audit_log(
            db=db,
            user_id=current_user.id,
            resource="/internal/data",
            action="GET",
            decision="DENY",
            reason="policy_denied",
        )

        raise HTTPException(status_code=403, detail="Access denied by security policy")

    # 4. ALLOW → create audit log
    create_audit_log(
        db=db,
        user_id=current_user.id,
        resource="/internal/data",
        action="GET",
        decision="ALLOW",
        reason="policy_allowed",
    )

    # 5. Forward request to internal service
    response = await forward_request("GET", "/internal/data")

    return response.json()
