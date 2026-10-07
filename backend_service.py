from fastapi import FastAPI

app = FastAPI(title="CloudShield Internal Service")


@app.get("/internal/data")
async def internal_data():
    return {"service": "internal-service", "message": "Sensitive internal data"}


@app.get("/internal/status")
async def internal_status():
    return {"service": "internal-service", "status": "healthy"}
