from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.models.policy import Policy
from app.models.user import User
from app.services.policy_engine import check_policy


def create_test_database():
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )

    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return SessionLocal()


def setup_database():
    db = create_test_database()

    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="dummy",
        role="user",
    )

    admin = User(
        username="admin",
        email="admin@example.com",
        hashed_password="dummy",
        role="admin",
    )

    db.add_all([user, admin])

    policies = [
        Policy(
            name="User Profile",
            role="user",
            resource="/profile",
            action="GET",
            effect="ALLOW",
            enabled=True,
        ),
        Policy(
            name="User Admin Deny",
            role="user",
            resource="/admin",
            action="GET",
            effect="DENY",
            enabled=True,
        ),
        Policy(
            name="Admin Access",
            role="admin",
            resource="/admin",
            action="GET",
            effect="ALLOW",
            enabled=True,
        ),
    ]

    db.add_all(policies)
    db.commit()

    return db, user, admin


def test_user_profile_allowed():
    db, user, admin = setup_database()

    assert check_policy(db, user, "/profile", "GET") is True

    db.close()


def test_user_admin_denied():
    db, user, admin = setup_database()

    assert check_policy(db, user, "/admin", "GET") is False

    db.close()


def test_admin_admin_allowed():
    db, user, admin = setup_database()

    assert check_policy(db, admin, "/admin", "GET") is True

    db.close()
