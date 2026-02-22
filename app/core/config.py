import os

class Config:
    MODEL_PATH = os.getenv("MODEL_PATH", "artifacts/cnn_model.pt")
    ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png"}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit for uploaded images

config = Config()