from pydantic import BaseModel
from typing import Optional

class PredictionResponse(BaseModel):
    """Response model for prediction"""
    prediction: str
    confidence: float
    cat_probability: float
    dog_probability: float
    success: bool
    error: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "prediction": "dog",
                "confidence": 0.9876,
                "cat_probability": 0.0124,
                "dog_probability": 0.9876,
                "success": True,
                "error": None
            }
        }

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool