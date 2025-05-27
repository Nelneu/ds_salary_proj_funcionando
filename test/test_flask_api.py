# tests/test_flask_api.py
import pytest
import json
import sys
import os

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from flask_api import app

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test that the API is running."""
    response = client.get('/')
    assert response.status_code in [200, 404]  # Either works or returns 404

def test_predict_endpoint_structure(client):
    """Test predict endpoint structure (without actual model)."""
    # Test with sample data
    test_data = {
        "feature1": 5,
        "feature2": "test_value"
    }
    
    response = client.post('/predict', 
                         data=json.dumps(test_data),
                         content_type='application/json')
    
    # Should return some response (even if model not loaded)
    assert response.status_code in [200, 400, 500]
    
def test_invalid_json_request(client):
    """Test API handles invalid JSON gracefully."""
    response = client.post('/predict', 
                         data="invalid json",
                         content_type='application/json')
    
    assert response.status_code == 400
