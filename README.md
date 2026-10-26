# Customer Churn Prediction: SageMaker Pipelines & Drift Detection

[![Pipeline SDK](https://img.shields.io/badge/Orchestrator-SageMaker%20Pipelines%20SDK-orange)](src/churn_mlops/sagemaker_dag.py)
[![Model Governance](https://img.shields.io/badge/Drift%20Observability-Evidently%20AI%20%7C%20PSI-blue)](src/churn_mlops/pipeline.py)
[![Code Standard](https://img.shields.io/badge/Clean%20Code-Zero%20Notebooks%20%28Pure%20Python%29-brightgreen)](src/churn_mlops)

Production-ready, reproducible Machine Learning pipeline for customer retention and churn prediction (**NTT DATA** production pattern).

This repository converts exploratory Jupyter Notebooks into a modular Python package and provisions a DAG using the **Amazon SageMaker Pipelines SDK**, featuring:
- **Zero Deserialization RCE Risk**: Replaced legacy `pickle.load` with safe JSON serialization.
- **Deterministic Data Contracts**: Eliminates missing category errors from unseeded `pd.get_dummies` by implementing robust feature transformers.
- **Automated Drift Detection**: Population Stability Index (PSI) and feature drift monitors that trigger automated retraining pipelines upon statistical degradation.

---

## 🏛️ Pipeline DAG Architecture

```
[Raw Store Data]
       │
       ▼
[ProcessingStep: Feature Engineering] ──> Deterministic normalization
       │
       ▼
[TrainingStep: XGBoost Estimator]
       │
       ▼
[EvaluationStep: ROC-AUC Scoring]
       │
       ▼
[ConditionStep: AUC >= 0.82 ?]
       ├── True  ──> [RegisterModelPackage in Model Registry]
       └── False ──> [Notify Data Science Team / Alert CloudWatch]
```

---

## 🚀 Local Verification

```bash
export PYTHONPATH=src
python -m pytest tests/ -v
```
