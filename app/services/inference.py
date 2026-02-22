import os
import shutil
from typing import Optional, Dict
from fastapi import UploadFile
from pathlib import Path
from app.models.model import ImageClassifier
from app.core.config import settings

class InferenceService:
    """Service for handling inference operations"""
    
    _instance: Optional[ImageClassifier] = None
    
    @classmethod
    def get_classifier(cls) -> ImageClassifier:
        """Singleton pattern for model loading"""
        if cls._instance is None:
            cls._instance = ImageClassifier(
                model_path=settings.MODEL_PATH,
                device=settings.DEVICE
            )
        return cls._instance
    
    @staticmethod
    def save_upload_file(upload_file: UploadFile) -> str:
        """
        Save uploaded file temporarily
        
        Args:
            upload_file: FastAPI UploadFile object
            
        Returns:
            Path to saved file
        """
        try:
            # Validate file extension
            file_ext = upload_file.filename.split('.')[-1].lower()
            if file_ext not in settings.ALLOWED_EXTENSIONS:
                raise ValueError(f"File type .{file_ext} not allowed")
            
            # Create unique filename
            file_path = settings.upload_dir_path / upload_file.filename
            
            # Save file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
            
            return str(file_path)
            
        except Exception as e:
            raise Exception(f"Failed to save file: {str(e)}")
    
    @staticmethod
    def cleanup_file(file_path: str) -> None:
        """Remove temporary file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Warning: Could not delete {file_path}: {str(e)}")
    
    @staticmethod
    async def predict_image(upload_file: UploadFile) -> Dict:
        """
        Predict image class
        
        Args:
            upload_file: Uploaded image file
            
        Returns:
            Prediction result dictionary
        """
        file_path = None
        try:
            # Save file
            file_path = InferenceService.save_upload_file(upload_file)
            
            # Get classifier and predict
            classifier = InferenceService.get_classifier()
            result = classifier.predict(file_path)
            
            return result
            
        finally:
            # Cleanup
            if file_path:
                InferenceService.cleanup_file(file_path)