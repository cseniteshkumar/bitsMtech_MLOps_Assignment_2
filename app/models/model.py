import torch
import torch.nn as nn
from pathlib import Path
from typing import Tuple, Dict
import torchvision.transforms as transforms
from PIL import Image
import os

class Cnn(nn.Module):
    def __init__(self):
        super(Cnn, self).__init__()
        
        # Layer 1: 224 -> 55 -> 27
        self.layer1 = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, stride=2, padding=1), # Added padding=1
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )
        
        # Layer 2: 27 -> 7 -> 3
        self.layer2 = nn.Sequential(
            nn.Conv2d(16, 32, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )
        
        # Layer 3: 3 -> 1
        self.layer3 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            # MaxPool here might make the feature map too small (0 or 1)
        )
        
        # Global Average Pooling is more modern than fixed Linear sizes
        self.adaptive_pool = nn.AdaptiveAvgPool2d((1, 1))
        
        self.fc1 = nn.Linear(64, 10)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(10, 2)
        self.relu = nn.ReLU()
        
    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = self.layer3(out)
        
        # Modern pooling: ensures the output is always the right size for FC layers
        out = self.adaptive_pool(out)
        out = torch.flatten(out, 1) # Cleaner than out.view()
        
        out = self.relu(self.fc1(out))
        out = self.dropout(out) # Apply dropout during forward pass
        out = self.fc2(out)
        return out



class ImageClassifier:
    """Wrapper for model inference"""
    
    def __init__(self, model_path: str, device: str = "cpu"):
        self.device = torch.device(device)
        self.model = self._load_model(model_path)
        self.class_names = {0: "cat", 1: "dog"}
        
        # Normalization values for ImageNet
        self.norm_mean = [0.485, 0.456, 0.406]
        self.norm_std = [0.229, 0.224, 0.225]
        
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(self.norm_mean, self.norm_std)
        ])
    
    def _load_model(self, model_path: str) -> nn.Module:
        """Load model from checkpoint"""
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}")
        
        model = Cnn().to(self.device)
        checkpoint = torch.load(model_path, map_location=self.device)
        model.load_state_dict(checkpoint)
        model.eval()
        return model
    
    def predict(self, image_path: str) -> Dict[str, any]:
        """
        Predict class for a single image
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary with prediction, confidence, and class probabilities
        """
        try:
            # Load and preprocess image
            image = Image.open(image_path).convert('RGB')
            image_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            # Inference
            with torch.no_grad():
                logits = self.model(image_tensor)
                probs = torch.softmax(logits, dim=1)
                
                pred_class = probs.argmax(dim=1).item()
                confidence = probs[0, pred_class].item()
                cat_prob = probs[0, 0].item()
                dog_prob = probs[0, 1].item()
            
            return {
                "prediction": self.class_names[pred_class],
                "confidence": round(confidence, 4),
                "cat_probability": round(cat_prob, 4),
                "dog_probability": round(dog_prob, 4),
                "success": True
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "prediction": None,
                "confidence": None
            }