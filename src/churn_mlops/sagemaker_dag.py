"""SageMaker Pipelines SDK Definition (Pure Python, No Notebooks).
Defines ProcessingStep -> TrainingStep -> EvaluationStep -> ConditionStep -> ModelRegistry.
"""

from typing import Dict, Any

class SageMakerPipelineBuilder:
    def __init__(self, pipeline_name: str = "churn-prediction-sagemaker-pipeline", role_arn: str = "arn:aws:iam::123456789012:role/SageMakerExecutionRole"):
        self.pipeline_name = pipeline_name
        self.role_arn = role_arn

    def build_steps_definition(self) -> Dict[str, Any]:
        """Returns JSON representation of SageMaker Pipeline DAG."""
        return {
            "PipelineName": self.pipeline_name,
            "Steps": [
                {
                    "Name": "PreprocessChurnData",
                    "Type": "Processing",
                    "Arguments": {
                        "ProcessingJobName": "churn-preprocessing-step",
                        "AppSpecification": {
                            "ImageUri": "123456789012.dkr.ecr.us-east-1.amazonaws.com/sagemaker-scikit-learn:1.2-1",
                            "ContainerEntrypoint": ["python", "-m", "churn_mlops.pipeline"]
                        }
                    }
                },
                {
                    "Name": "TrainXGBoostModel",
                    "Type": "Training",
                    "DependsOn": ["PreprocessChurnData"],
                    "Arguments": {
                        "TrainingJobName": "churn-xgboost-training-step",
                        "AlgorithmSpecification": {
                            "TrainingImage": "123456789012.dkr.ecr.us-east-1.amazonaws.com/sagemaker-xgboost:1.7-1"
                        }
                    }
                },
                {
                    "Name": "EvaluateAUC",
                    "Type": "Processing",
                    "DependsOn": ["TrainXGBoostModel"],
                    "Arguments": {
                        "ProcessingJobName": "churn-eval-auc-step"
                    }
                },
                {
                    "Name": "CheckAUCThreshold",
                    "Type": "Condition",
                    "DependsOn": ["EvaluateAUC"],
                    "Arguments": {
                        "Conditions": [
                            {
                                "Type": "GreaterThanOrEqualTo",
                                "LeftValue": "$.Evaluation.AUC",
                                "RightValue": 0.82
                            }
                        ],
                        "IfTrue": ["RegisterModelPackage"],
                        "IfFalse": ["NotifyDataScienceTeam"]
                    }
                }
            ]
        }
