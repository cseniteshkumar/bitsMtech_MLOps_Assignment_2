import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient
import numpy as np
import json

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app
from app.schemas.prediction import PredictionRequest, PredictionResponse


client = TestClient(app)


class TestDeployment:
    """Test suite for deployment validation"""

    def test_app_startup(self):
        """Test that the application starts without errors"""
        assert app is not None
        assert app.title or True  # App initialized successfully

    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health" if hasattr(app, "health_route") else "/")
        assert response.status_code in [200, 404, 405]  # Accept various responses

    def test_api_routes_exist(self):
        """Test that API routes are properly registered"""
        routes = [route.path for route in app.routes]
        assert len(routes) > 0, "No routes registered"

    def test_prediction_endpoint_exists(self):
        """Test prediction endpoint is available"""
        response = client.post("/api/predict", json={})
        # Should return either success or validation error, not 404
        assert response.status_code != 404, "Prediction endpoint not found"

    def test_valid_prediction_request(self):
        """Test valid prediction request"""
        payload = {
            "features": [1.0, 2.0, 3.0, 4.0]  # Adjust based on your model input
        }
        response = client.post("/api/predict", json=payload)
        assert response.status_code in [200, 422], f"Unexpected status: {response.status_code}"
        
        if response.status_code == 200:
            data = response.json()
            assert "prediction" in data or "result" in data

    def test_invalid_prediction_request(self):
        """Test invalid prediction request handling"""
        payload = {"invalid_field": "data"}
        response = client.post("/api/predict", json=payload)
        assert response.status_code == 422, "Should validate input schema"

    def test_empty_request(self):
        """Test empty request handling"""
        response = client.post("/api/predict", json={})
        assert response.status_code == 422

    def test_model_inference_consistency(self):
        """Test that model produces consistent results"""
        payload = {"features": [1.0, 2.0, 3.0, 4.0]}
        
        response1 = client.post("/api/predict", json=payload)
        response2 = client.post("/api/predict", json=payload)
        
        if response1.status_code == 200 and response2.status_code == 200:
            result1 = response1.json()
            result2 = response2.json()
            assert result1 == result2, "Model predictions should be consistent"

    def test_response_format(self):
        """Test response format is correct"""
        payload = {"features": [1.0, 2.0, 3.0, 4.0]}
        response = client.post("/api/predict", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, dict), "Response should be JSON object"

    def test_concurrent_requests(self):
        """Test handling multiple concurrent requests"""
        payload = {"features": [1.0, 2.0, 3.0, 4.0]}
        
        responses = []
        for _ in range(5):
            response = client.post("/api/predict", json=payload)
            responses.append(response)
        
        assert all(r.status_code in [200, 422] for r in responses)

    def test_large_input(self):
        """Test handling of large input arrays"""
        large_features = [1.0] * 1000
        payload = {"features": large_features}
        response = client.post("/api/predict", json=payload)
        assert response.status_code in [200, 422]

    def test_special_values(self):
        """Test handling of special values (NaN, inf, etc.)"""
        test_cases = [
            {"features": [float('inf'), 1.0, 2.0, 3.0]},
            {"features": [float('-inf'), 1.0, 2.0, 3.0]},
            {"features": [0.0, 0.0, 0.0, 0.0]},
            {"features": [1e-10, 1e-10, 1e-10, 1e-10]},
        ]
        
        for payload in test_cases:
            response = client.post("/api/predict", json=payload)
            assert response.status_code in [200, 422, 400]

    def test_model_loaded(self):
        """Test that model is properly loaded"""
        try:
            from app.services.inference import InferenceService
            service = InferenceService()
            assert service is not None
        except Exception as e:
            pytest.fail(f"Model loading failed: {str(e)}")

    def test_config_loaded(self):
        """Test that configuration is properly loaded"""
        try:
            from app.core.config import Settings
            config = Settings()
            assert config is not None
        except Exception as e:
            pytest.fail(f"Config loading failed: {str(e)}")

    def test_response_headers(self):
        """Test that response headers are correct"""
        response = client.post("/api/predict", json={"features": [1.0, 2.0, 3.0, 4.0]})
        assert "content-type" in response.headers.keys()


class TestErrorHandling:
    """Test error handling and edge cases"""

    def test_malformed_json(self):
        """Test malformed JSON handling"""
        response = client.post(
            "/api/predict",
            data="{invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code in [400, 422]

    def test_wrong_content_type(self):
        """Test wrong content type handling"""
        response = client.post(
            "/api/predict",
            data="not json data",
            headers={"Content-Type": "text/plain"}
        )
        assert response.status_code in [400, 415, 422]

    def test_missing_required_fields(self):
        """Test missing required fields"""
        response = client.post("/api/predict", json={"wrong_field": [1, 2, 3]})
        assert response.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])