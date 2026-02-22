from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from app.services.inference import predict_single_image
from app.core.config import MODEL_PATH
import os

router = APIRouter()

@router.post("/predict/")
async def upload_image(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        return JSONResponse(content={"error": "File type not supported"}, status_code=400)

    # Save the uploaded file temporarily
    file_location = f"temp/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Make prediction
    prediction = predict_single_image(file_location, MODEL_PATH)

    # Clean up the temporary file
    os.remove(file_location)

    return JSONResponse(content=prediction)