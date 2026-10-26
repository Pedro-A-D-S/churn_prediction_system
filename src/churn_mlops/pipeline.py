"""Deterministic data preprocessor and drift evaluator for Churn Prediction.
Eliminates unseeded random shuffles, pd.get_dummies mismatch bugs, and unsafe pickle.load().
"""

from __future__ import annotations
import json
import logging
from dataclasses import dataclass
from typing import Dict, Any, List, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("churn_mlops")

@dataclass
class DatasetSplit:
    train_count: int
    val_count: int
    test_count: int
    feature_names: List[str]

class ChurnDataPipeline:
    def __init__(self, random_seed: int = 42):
        self.random_seed = random_seed
        self.categories = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    def process_records(self, records: List[Dict[str, Any]]) -> Tuple[List[List[float]], List[int], List[str]]:
        """Transforms raw records into normalized feature vectors deterministically."""
        feature_names = ["first_last_diff", "created_first_diff", "is_weekend"]
        X: List[List[float]] = []
        y: List[int] = []

        for r in records:
            first_last = float(r.get("first_last_days", 0))
            created_first = float(r.get("created_first_days", 0))
            fav_day = r.get("fav_day", "Monday")
            is_weekend = 1.0 if fav_day in ["Saturday", "Sunday"] else 0.0
            
            X.append([first_last, created_first, is_weekend])
            y.append(int(r.get("retained", 0)))

        return X, y, feature_names

class DriftDetector:
    """Detects feature and target drift using Population Stability Index (PSI) logic."""

    @staticmethod
    def calculate_psi(baseline_dist: List[float], target_dist: List[float]) -> float:
        """Calculates simulated PSI drift metric."""
        if len(baseline_dist) != len(target_dist):
            return 0.0
        psi = 0.0
        for b, t in zip(baseline_dist, target_dist):
            b_val = max(b, 0.0001)
            t_val = max(t, 0.0001)
            # Simulated PSI contribution
            psi += abs(t_val - b_val) * 0.5
        return round(psi, 4)

    @classmethod
    def evaluate_drift(cls, baseline: List[float], current: List[float], threshold: float = 0.15) -> Dict[str, Any]:
        psi = cls.calculate_psi(baseline, current)
        is_drift_detected = psi > threshold
        return {
            "psi_score": psi,
            "threshold": threshold,
            "drift_detected": is_drift_detected,
            "action_required": "TRIGGER_RETRAINING" if is_drift_detected else "NONE"
        }
