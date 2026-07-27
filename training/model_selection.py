import logging
import pandas as pd
from typing import Dict, Any, Tuple
from sklearn.model_selection import cross_validate, StratifiedKFold
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression

logger = logging.getLogger(__name__)

def get_baseline_models(random_state: int) -> Dict[str, Any]:
    return {
        "LogisticRegression": LogisticRegression(random_state=random_state, max_iter=1000),
        "RandomForest": RandomForestClassifier(random_state=random_state),
        "ExtraTrees": ExtraTreesClassifier(random_state=random_state),
        "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric="logloss", random_state=random_state),
        "LightGBM": LGBMClassifier(random_state=random_state, verbose=-1),
        "CatBoost": CatBoostClassifier(random_state=random_state, verbose=0)
    }

def evaluate_baselines(X_train: pd.DataFrame, y_train: pd.Series, random_state: int) -> pd.DataFrame:
    """
    Evaluates baseline models using 5-fold cross validation.
    Returns a dataframe of the results for comparison.
    """
    models = get_baseline_models(random_state)
    results = []
    
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)
    
    for name, model in models.items():
        logger.info(f"Evaluating {name}...")
        scores = cross_validate(
            model, X_train, y_train, 
            cv=cv, 
            scoring=['roc_auc', 'f1', 'accuracy'], 
            n_jobs=-1
        )
        
        results.append({
            "Model": name,
            "ROC-AUC": scores["test_roc_auc"].mean(),
            "F1": scores["test_f1"].mean(),
            "Accuracy": scores["test_accuracy"].mean()
        })
        
    results_df = pd.DataFrame(results).sort_values(by="ROC-AUC", ascending=False)
    return results_df
