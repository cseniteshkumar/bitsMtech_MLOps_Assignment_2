from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from app.api.routes import router
from app.core.config import settings

app = FastAPI()

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Image Prediction API"}

# Additional middleware or configurations can be added here if needed.