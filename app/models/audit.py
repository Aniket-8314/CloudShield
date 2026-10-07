from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone

from app.core.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=False)
    resource = Column(String, nullable=False)
    action = Column(String, nullable=False)

    decision = Column(String, nullable=False)
    reason = Column(String, nullable=False)

    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
