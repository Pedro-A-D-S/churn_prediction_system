import pytest
from churn_mlops.pipeline import ChurnDataPipeline, DriftDetector
from churn_mlops.sagemaker_dag import SageMakerPipelineBuilder

def test_data_pipeline_deterministic_processing():
    pipeline = ChurnDataPipeline(random_seed=42)
    sample_records = [
        {"custid": "C1", "first_last_days": 120, "created_first_days": 10, "fav_day": "Monday", "retained": 1},
        {"custid": "C2", "first_last_days": 5, "created_first_days": 2, "fav_day": "Sunday", "retained": 0}
    ]
    X, y, feature_names = pipeline.process_records(sample_records)
    
    assert len(X) == 2
    assert len(y) == 2
    assert y == [1, 0]
    assert X[0][2] == 0.0 # Monday not weekend
    assert X[1][2] == 1.0 # Sunday is weekend

def test_drift_detector_clean_distribution():
    baseline = [0.2, 0.3, 0.5]
    current = [0.21, 0.29, 0.50]
    drift = DriftDetector.evaluate_drift(baseline, current, threshold=0.10)
    
    assert drift["drift_detected"] is False
    assert drift["action_required"] == "NONE"

def test_drift_detector_triggers_retraining():
    baseline = [0.1, 0.2, 0.7]
    shifted = [0.6, 0.3, 0.1]
    drift = DriftDetector.evaluate_drift(baseline, shifted, threshold=0.15)
    
    assert drift["drift_detected"] is True
    assert drift["action_required"] == "TRIGGER_RETRAINING"

def test_sagemaker_pipeline_builder():
    builder = SageMakerPipelineBuilder()
    dag = builder.build_steps_definition()
    assert dag["PipelineName"] == "churn-prediction-sagemaker-pipeline"
    assert len(dag["Steps"]) == 4
    assert dag["Steps"][3]["Name"] == "CheckAUCThreshold"
