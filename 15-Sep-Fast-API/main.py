import asyncio

from fastapi import FastAPI, HTTPException
from models import HealthResponse, PredictionRequest, PredictionResponse

app = FastAPI(
    title="FastAPI ML Service",
    description="Backend API for a mock machine learning service",
    version="1.0.0"
)


@app.get("/", response_model=HealthResponse)
async def root():
    return {
        "status": "running",
        "service": "FastAPI ML Service"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    return {
        "status": "healthy",
        "service": "prediction-api"
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(data: PredictionRequest):

    score = (
        data.salary / 100000
        + data.experience / 20
        + data.age / 100
    ) / 3

    prediction = "high" if score >= 0.6 else "low"

    return {
        "prediction": prediction,
        "score": round(score, 2),
        "message": "Prediction generated successfully"
    }

@app.get("/users/{user_id}")
async def get_user(user_id: int):

    if user_id != 1:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": 1,
        "name": "Yash"
    }

@app.get("/async-demo")
async def async_demo():
    await asyncio.sleep(2)

    return {
        "message": "Async operation completed",
        "status": "success"
    }