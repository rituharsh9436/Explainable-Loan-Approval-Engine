import logging
import shap
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix
)

logger = logging.getLogger(__name__)

def evaluate_model(model, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, Any]:
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred)),
        "recall": float(recall_score(y_test, y_pred)),
        "f1_score": float(f1_score(y_test, y_pred)),
        "roc_auc": float(roc_auc_score(y_test, y_prob)),
        "pr_auc": float(average_precision_score(y_test, y_prob)),
    }
    
    cm = confusion_matrix(y_test, y_pred)
    metrics["confusion_matrix"] = {
        "tn": int(cm[0, 0]),
        "fp": int(cm[0, 1]),
        "fn": int(cm[1, 0]),
        "tp": int(cm[1, 1])
    }
    
    logger.info(f"Test Set Evaluation Metrics: {metrics}")
    return metrics

def check_shap_compatibility(model, X_test: pd.DataFrame):
    """
    Sanity checks if SHAP TreeExplainer can explain this model properly.
    """
    logger.info("Validating SHAP compatibility...")
    try:
        explainer = shap.TreeExplainer(model)
        # Just explain the first row as a test
        shap_values = explainer.shap_values(X_test.iloc[[0]])
        logger.info("SHAP compatibility check passed.")
        return True
    except Exception as e:
        logger.error(f"SHAP compatibility check failed: {e}")
        return False
