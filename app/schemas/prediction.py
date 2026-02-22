from pydantic import BaseModel, ConfigDict
from typing import Optional

from pydantic import BaseModel, ConfigDict

class PredictionRequest(BaseModel):
    """Request schema for predictions"""
    features: list[float]
    
    model_config = ConfigDict(from_attributes=True)

# class PredictionResponse(BaseModel):
#     """Response schema for predictions"""
#     prediction: float
    
#     model_config = ConfigDict(from_attributes=True)

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