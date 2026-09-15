from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    age: int = Field(..., ge=18, le=100)
    salary: float = Field(..., ge=0)
    experience: int = Field(..., ge=0, le=50)


class PredictionResponse(BaseModel):
    prediction: str
    score: float
    message: str


class HealthResponse(BaseModel):
    status: str
    service: str