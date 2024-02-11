from fastapi.testclient import TestClient

from unittest.mock import Mock
from src.serving.model import BertPredictor

def mock_predict(text):
    return ['positive' for _ in text]

BertPredictor.from_model_registry = Mock(return_value=Mock(predict=mock_predict))



def test_predict():
    from src.serving.fastapi import app
    client = TestClient(app)

    payload = {
        "text": ["This is a test sentence.", "Here's another one!"]
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == len(payload['text'])
