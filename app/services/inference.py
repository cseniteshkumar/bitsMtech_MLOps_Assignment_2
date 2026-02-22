from fastapi import UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import torch
from torchvision import transforms
from app.models.model import load_model

class InferenceService:
    def __init__(self, model_path: str, device: str):
        self.device = device
        self.model = load_model(model_path, device)

    def preprocess_image(self, image: UploadFile) -> torch.Tensor:
        img = Image.open(image.file).convert("RGB")
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        img_tensor = transform(img).unsqueeze(0).to(self.device)
        return img_tensor

    def predict(self, image: UploadFile) -> dict:
        img_tensor = self.preprocess_image(image)
        with torch.inference_mode():
            logits = self.model(img_tensor)
            probs = logits.softmax(dim=1)
            pred_class = probs.argmax(dim=1).item()
            confidence = probs[0, pred_class].item()
        
        class_names = {0: "Cat", 1: "Dog"}
        return {
            "prediction": class_names[pred_class],
            "confidence": confidence
        }