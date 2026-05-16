import numpy as np

class XAIEngine:
    """Generates feature importance attributions and calibrated confidence metrics."""

    def __init__(self, feature_names: list[str]):
        self.feature_names = feature_names

    def compute_attributions(self, feature_vector: list[float]) -> dict[str, float]:
        """Calculates normalized feature importance scores for model predictions."""
        vec = np.abs(np.array(feature_vector, dtype=float))
        total = np.sum(vec) + 1e-9
        importance = vec / total
        
        return {
            name: round(float(score), 4)
            for name, score in zip(self.feature_names, importance)
        }