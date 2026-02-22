import os
from pathlib import Path

class Settings:
    # Model Configuration
    MODEL_PATH: str = os.getenv("MODEL_PATH", "artifacts/cnn_model.pt")
    DEVICE: str = os.getenv("DEVICE", "cpu")  # cuda, mps, or cpu
    
    # File Upload Configuration
    UPLOAD_DIR: str = "temp_uploads"
    ALLOWED_EXTENSIONS: set = {"jpg", "jpeg", "png"}
    MAX_FILE_SIZE: int = 16 * 1024 * 1024  # 16 MB
    
    # API Configuration
    API_TITLE: str = "Dog vs Cat Classifier API"
    API_VERSION: str = "1.0.0"
    
    @property
    def upload_dir_path(self) -> Path:
        path = Path(self.UPLOAD_DIR)
        path.mkdir(parents=True, exist_ok=True)
        return path

settings = Settings()