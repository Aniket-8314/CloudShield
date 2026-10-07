from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.services.policy_engine import check_policy
from app.services.rate_limiter import check_rate_limit


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
    }


@router.get("/profile")
def profile(current_user: User = Depends(get_current_user), db=Depends(get_db)):
    check_rate_limit(current_user.id)

    allowed = check_policy(db, current_user, "/profile", "GET")

    if not allowed:
        raise HTTPException(status_code=403, detail="Access denied by security policy")

    return {"message": "Welcome to your profile", "user": current_user.username}


@router.get("/admin")
def admin_area(current_user: User = Depends(get_current_user), db=Depends(get_db)):

    allowed = check_policy(db, current_user, "/admin", "GET")

    if not allowed:
        raise HTTPException(status_code=403, detail="Access denied by security policy")

    return {"message": "Welcome to the admin area"}
