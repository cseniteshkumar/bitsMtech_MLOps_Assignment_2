from pathlib import Path
import torch
import torchvision.transforms as transforms
from PIL import Image

class ImageClassifier:
    def __init__(self, model_path: str, device: str):
        self.device = device
        self.model = self.load_model(model_path)

    def load_model(self, model_path: str):
        model = Cnn().to(self.device)  # Assuming Cnn is defined elsewhere
        model.load_state_dict(torch.load(model_path, map_location=self.device))
        model.eval()
        return model

    def preprocess_image(self, image_path: str):
        norm_mean = [0.485, 0.456, 0.406]
        norm_std = [0.229, 0.224, 0.225]
        
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(norm_mean, norm_std)
        ])
        
        image = Image.open(image_path).convert('RGB')
        return transform(image).unsqueeze(0).to(self.device)

    def predict(self, image_path: str):
        image_tensor = self.preprocess_image(image_path)
        with torch.inference_mode():
            logits = self.model(image_tensor)
            probs = logits.softmax(dim=1)
            pred_class = probs.argmax(dim=1).item()
            confidence = probs[0, pred_class].item()
            return pred_class, confidence