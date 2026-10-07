from app.models.policy import Policy


def seed_policies(db):

    existing = db.query(Policy).count()

    if existing > 0:
        return

    policies = [
        Policy(
            name="User profile access",
            role="user",
            resource="/profile",
            action="GET",
            effect="ALLOW",
        ),
        Policy(
            name="User admin restriction",
            role="user",
            resource="/admin",
            action="GET",
            effect="DENY",
        ),
        Policy(
            name="Admin access",
            role="admin",
            resource="/admin",
            action="GET",
            effect="ALLOW",
        ),
        Policy(
            name="User internal data access",
            role="user",
            resource="/internal/data",
            action="GET",
            effect="ALLOW",
        ),
    ]

    db.add_all(policies)
    db.commit()
