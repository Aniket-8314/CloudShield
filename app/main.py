from fastapi import FastAPI

from app.core.database import Base, engine, SessionLocal
from app.core.seed import seed_policies

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.gateway import router as gateway_router
from app.api.audit import router as audit_router

from app.models.user import User
from app.models.policy import Policy
from app.models.audit import AuditLog

from app.middleware.security import SecurityHeadersMiddleware

Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    seed_policies(db)
finally:
    db.close()


app = FastAPI(
    title="CloudShield", description="Zero-Trust Secure Access Gateway", version="1.0.0"
)

app.add_middleware(SecurityHeadersMiddleware)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(gateway_router)
app.include_router(audit_router)


@app.get("/")
async def root():
    return {"service": "CloudShield", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
