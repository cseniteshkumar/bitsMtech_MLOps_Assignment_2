import pytest
import torch
import numpy as np
import sys
import os
from pathlib import Path
from PIL import Image
import tempfile
import time

# Add parent directory to path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models.model import Cnn, ImageClassifier
from app.core.config import settings


class TestSmokeTests:
    """Smoke tests to validate core application functionality"""

    @pytest.fixture(scope="class")
    def model_path(self):
        """Get model path"""
        return os.path.join(
            os.path.dirname(__file__),
            '../artifacts/cnn_model.pt'
        )

    @pytest.fixture(scope="class")
    def test_image(self):
        """Create a temporary test image"""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            img = Image.new('RGB', (224, 224), color=(73, 109, 137))
            img.save(tmp.name)
            yield tmp.name
        os.unlink(tmp.name)

    # ============ MODEL ARCHITECTURE TESTS ============
    def test_01_cnn_model_instantiation(self):
        """Test 1: Verify CNN model can be instantiated"""
        try:
            model = Cnn()
            assert model is not None, "CNN model is None"
            assert isinstance(model, torch.nn.Module), "CNN is not a PyTorch Module"
        except Exception as e:
            pytest.fail(f"CNN model instantiation failed: {str(e)}")

    def test_02_cnn_model_structure(self):
        """Test 2: Verify CNN has required layers"""
        try:
            model = Cnn()
            assert hasattr(model, 'layer1'), "CNN missing layer1"
            assert hasattr(model, 'layer2'), "CNN missing layer2"
            assert hasattr(model, 'layer3'), "CNN missing layer3"
            assert hasattr(model, 'fc1'), "CNN missing fc1"
            assert hasattr(model, 'fc2'), "CNN missing fc2"
            assert hasattr(model, 'adaptive_pool'), "CNN missing adaptive_pool"
        except Exception as e:
            pytest.fail(f"CNN layer check failed: {str(e)}")

    def test_03_cnn_forward_pass(self):
        """Test 3: Verify CNN forward pass produces correct output shape"""
        try:
            model = Cnn()
            model.eval()
            
            dummy_input = torch.randn(1, 3, 224, 224)
            
            with torch.no_grad():
                output = model(dummy_input)
            
            assert output is not None, "Model output is None"
            assert output.shape == (1, 2), f"Expected output shape (1, 2), got {output.shape}"
        except Exception as e:
            pytest.fail(f"CNN forward pass failed: {str(e)}")

    def test_04_cnn_batch_inference(self):
        """Test 4: Verify CNN works with batch inputs"""
        try:
            model = Cnn()
            model.eval()
            
            batch_input = torch.randn(4, 3, 224, 224)
            
            with torch.no_grad():
                output = model(batch_input)
            
            assert output.shape == (4, 2), f"Expected batch output shape (4, 2), got {output.shape}"
        except Exception as e:
            pytest.fail(f"CNN batch inference failed: {str(e)}")

    # ============ MODEL CHECKPOINT TESTS ============
    def test_05_model_checkpoint_exists(self, model_path):
        """Test 5: Verify model checkpoint file exists"""
        assert os.path.exists(model_path), f"Model checkpoint not found at {model_path}"
        assert os.path.getsize(model_path) > 0, "Model checkpoint is empty"

    def test_06_model_checkpoint_loads(self, model_path):
        """Test 6: Verify model checkpoint is valid PyTorch format"""
        try:
            checkpoint = torch.load(model_path, map_location='cpu')
            assert isinstance(checkpoint, dict), "Checkpoint should be a dictionary"
            assert len(checkpoint) > 0, "Checkpoint is empty"
        except Exception as e:
            pytest.fail(f"Model checkpoint loading failed: {str(e)}")

    # ============ IMAGE CLASSIFIER TESTS ============
    def test_07_image_classifier_init(self, model_path):
        """Test 7: Verify ImageClassifier initialization"""
        try:
            classifier = ImageClassifier(model_path=model_path, device='cpu')
            assert classifier is not None, "ImageClassifier is None"
            assert classifier.model is not None, "Model is None in classifier"
            assert classifier.class_names == {0: "cat", 1: "dog"}, "Invalid class names"
        except Exception as e:
            pytest.fail(f"ImageClassifier initialization failed: {str(e)}")

    def test_08_image_classifier_transforms(self, model_path):
        """Test 8: Verify image transform pipeline is configured"""
        try:
            classifier = ImageClassifier(model_path=model_path, device='cpu')
            assert hasattr(classifier, 'transform'), "Missing transform attribute"
            assert classifier.transform is not None, "Transform is None"
        except Exception as e:
            pytest.fail(f"ImageClassifier transform check failed: {str(e)}")

    def test_09_image_classifier_invalid_model_path(self):
        """Test 9: Verify ImageClassifier raises error with invalid model path"""
        with pytest.raises(FileNotFoundError):
            ImageClassifier(model_path="/invalid/nonexistent/path.pt", device='cpu')

    # ============ INFERENCE TESTS ============
    def test_10_inference_with_valid_image(self, model_path, test_image):
        """Test 10: Verify inference produces valid output with real image"""
        try:
            classifier = ImageClassifier(model_path=model_path, device='cpu')
            result = classifier.predict(test_image)
            
            assert result is not None, "Prediction result is None"
            assert result['success'] is True, f"Prediction failed: {result.get('error')}"
            assert result['prediction'] in ['cat', 'dog'], "Invalid prediction class"
        except Exception as e:
            pytest.fail(f"Inference test failed: {str(e)}")

    def test_11_inference_output_structure(self, model_path, test_image):
        """Test 11: Verify inference output has required fields"""
        try:
            classifier = ImageClassifier(model_path=model_path, device='cpu')
            result = classifier.predict(test_image)
            
            required_keys = ['prediction', 'confidence', 'cat_probability', 'dog_probability', 'success']
            for key in required_keys:
                assert key in result, f"Missing key in result: {key}"
        except Exception as e:
            pytest.fail(f"Output structure test failed: {str(e)}")

    def test_12_inference_probability_validity(self, model_path, test_image):
        """Test 12: Verify probabilities are in valid range [0, 1]"""
        try:
            classifier = ImageClassifier(model_path=model_path, device='cpu')
            result = classifier.predict(test_image)
            
            assert 0.0 <= result['confidence'] <= 1.0, f"Invalid confidence: {result['confidence']}"
            assert 0.0 <= result['cat_probability'] <= 1.0, f"Invalid cat probability"
            assert 0.0 <= result['dog_probability'] <= 1.0, f"Invalid dog probability"
            
            # Verify probabilities sum to 1.0 (with small tolerance)
            total_prob = result['cat_probability'] + result['dog_probability']
            assert 0.99 <= total_prob <= 1.01, f"Probabilities don't sum to 1.0: {total_prob}"
        except Exception as e:
            pytest.fail(f"Probability validity test failed: {str(e)}")

    def test_13_inference_with_invalid_image(self, model_path):
        """Test 13: Verify inference handles invalid image gracefully"""
        try:
            classifier = ImageClassifier(model_path=model_path, device='cpu')
            result = classifier.predict("/invalid/path/image.jpg")
            
            assert result is not None, "Result is None"
            assert result['success'] is False, "Should fail with invalid path"
            assert 'error' in result, "Error message missing"
        except Exception as e:
            pytest.fail(f"Invalid image handling test failed: {str(e)}")

    # ============ DEVICE TESTS ============
    def test_14_cpu_device_placement(self, model_path):
        """Test 14: Verify model loads on CPU correctly"""
        try:
            classifier = ImageClassifier(model_path=model_path, device='cpu')
            assert classifier.device.type == 'cpu', "Device should be CPU"
            
            # Verify model parameters are on CPU
            for param in classifier.model.parameters():
                assert param.device.type == 'cpu', "Model parameters not on CPU"
        except Exception as e:
            pytest.fail(f"CPU device placement failed: {str(e)}")

    def test_15_cuda_device_if_available(self, model_path):
        """Test 15: Verify model loads on CUDA if available"""
        if torch.cuda.is_available():
            try:
                classifier = ImageClassifier(model_path=model_path, device='cuda')
                assert classifier.device.type == 'cuda', "Device should be CUDA"
            except Exception as e:
                pytest.fail(f"CUDA device placement failed: {str(e)}")
        else:
            pytest.skip("CUDA not available on this system")

    # ============ NORMALIZATION TESTS ============
    def test_16_normalization_parameters(self, model_path):
        """Test 16: Verify normalization parameters are correct"""
        try:
            classifier = ImageClassifier(model_path=model_path, device='cpu')
            assert classifier.norm_mean == [0.485, 0.456, 0.406], "Invalid normalization mean"
            assert classifier.norm_std == [0.229, 0.224, 0.225], "Invalid normalization std"
        except Exception as e:
            pytest.fail(f"Normalization parameters test failed: {str(e)}")

    def test_17_image_transform_output(self, model_path):
        """Test 17: Verify image transform produces correct tensor shape"""
        try:
            classifier = ImageClassifier(model_path=model_path, device='cpu')
            
            test_img = Image.new('RGB', (300, 300), color=(150, 150, 150))
            transformed = classifier.transform(test_img)
            
            assert isinstance(transformed, torch.Tensor), "Transform should return Tensor"
            assert transformed.shape == (3, 224, 224), f"Expected shape (3, 224, 224), got {transformed.shape}"
        except Exception as e:
            pytest.fail(f"Image transform test failed: {str(e)}")

    # ============ PERFORMANCE TESTS ============
    def test_18_inference_speed(self, model_path, test_image):
        """Test 18: Verify inference completes within acceptable time"""
        try:
            classifier = ImageClassifier(model_path=model_path, device='cpu')
            
            start_time = time.time()
            result = classifier.predict(test_image)
            elapsed_time = time.time() - start_time
            
            # CPU inference should complete within 5 seconds
            assert elapsed_time < 5.0, f"Inference too slow: {elapsed_time:.2f}s (max: 5s)"
        except Exception as e:
            pytest.fail(f"Performance test failed: {str(e)}")

    # ============ DEPENDENCY TESTS ============
    def test_19_pytorch_available(self):
        """Test 19: Verify PyTorch is properly installed"""
        assert torch is not None, "PyTorch not imported"
        assert hasattr(torch, '__version__'), "PyTorch version not available"

    def test_20_pillow_available(self):
        """Test 20: Verify Pillow is available for image processing"""
        assert Image is not None, "Pillow/PIL not imported"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])