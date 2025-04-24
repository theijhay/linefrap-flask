import numpy as np
import pytest
from app.utils import analytical_model, extract_roi_normalize


def test_analytical_model_shape():
    t = np.arange(5)
    out = analytical_model(t, 0.8, 0.5, 10, 0.5)
    assert out.shape == t.shape


def test_extract_roi_normalize_error():
    # Create a stack with less than 4 frames
    stack = np.ones((3,10,10))
    with pytest.raises(ValueError):
        extract_roi_normalize(stack)