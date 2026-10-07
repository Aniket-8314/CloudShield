from sqlalchemy import Column, Integer, String, Boolean

from app.core.database import Base


class Policy(Base):
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    role = Column(String, nullable=False)

    resource = Column(String, nullable=False)

    action = Column(String, nullable=False)

    effect = Column(String, nullable=False)

    enabled = Column(Boolean, default=True)
