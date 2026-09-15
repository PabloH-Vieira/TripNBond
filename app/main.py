from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title="TripNBond API",
    description="API para o MVP",
    version="0.1"
)

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Endpoint simples para verificar se a API está online.
    """
    return {"status":"ok","message":"TripNBond is up!"}