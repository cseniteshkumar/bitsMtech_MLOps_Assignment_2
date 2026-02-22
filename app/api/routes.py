from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Optional
from app.services.inference import InferenceService
from app.schemas.prediction import PredictionResponse, HealthResponse
from app.core.config import settings

router = APIRouter(prefix="/api", tags=["predictions"])

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        classifier = InferenceService.get_classifier()
        return HealthResponse(
            status="healthy",
            model_loaded=True
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Model loading failed: {str(e)}"
        )

@router.post("/predict", response_model=PredictionResponse)
async def predict_image(file: UploadFile = File(...)):
    """
    Predict if uploaded image is a cat or dog
    
    Args:
        file: Image file (jpg, jpeg, png)
        
    Returns:
        Prediction result with confidence scores
    """
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image (jpg, jpeg, png)"
        )
    
    # Validate file size
    file_size = len(await file.read())
    await file.seek(0)  # Reset file pointer
    
    if file_size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds {settings.MAX_FILE_SIZE / (1024*1024):.0f}MB limit"
        )
    
    try:
        # Perform inference
        result = await InferenceService.predict_image(file)
        
        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("error", "Prediction failed")
            )
        
        return PredictionResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction error: {str(e)}"
        )

@router.get("/")
async def root():
    """API root endpoint"""
    return {
        "title": settings.API_TITLE,
        "version": settings.API_VERSION,
        "endpoints": {
            "health": "/api/health",
            "predict": "/api/predict"
        }
    }