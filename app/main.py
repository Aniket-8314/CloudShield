from fastapi import FastAPI

app = FastAPI(
    title="CloudShield",
    description="Zero-Trust Secure Access Gateway",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {
        "service": "CloudShield",
        "status": "running"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }