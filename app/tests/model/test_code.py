import numpy as np
from src.model.training import compute_metrics

def test_compute_metrics():
    mock_logits = np.array([[2, 0.1], [0.1, 2], [2, 0.1]])
    mock_labels = np.array([0, 1, 0])

    output = compute_metrics((mock_logits, mock_labels))

    expected_accuracy = 1.0
    assert output['accuracy'] == expected_accuracy, f"Expected accuracy: {expected_accuracy}, but got: {output['accuracy']}"
