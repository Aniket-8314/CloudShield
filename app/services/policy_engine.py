from sqlalchemy.orm import Session

from app.models.policy import Policy
from app.models.user import User


def check_policy(db: Session, user: User, resource: str, action: str) -> bool:

    policies = (
        db.query(Policy)
        .filter(
            Policy.role == user.role,
            Policy.resource == resource,
            Policy.action == action,
            Policy.enabled == True,
        )
        .all()
    )

    for policy in policies:
        if policy.effect.upper() == "DENY":
            return False

        if policy.effect.upper() == "ALLOW":
            return True

    # Default deny
    return False
