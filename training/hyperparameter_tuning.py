import optuna
import logging
from sklearn.model_selection import cross_val_score, StratifiedKFold
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from typing import Any, Tuple

logger = logging.getLogger(__name__)

def tune_xgboost(X_train, y_train, random_state: int, n_trials: int) -> Tuple[Any, dict]:
    def objective(trial):
        params = {
            "n_estimators": trial.suggest_int("n_estimators", 50, 300),
            "max_depth": trial.suggest_int("max_depth", 3, 10),
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
            "subsample": trial.suggest_float("subsample", 0.6, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
            "min_child_weight": trial.suggest_int("min_child_weight", 1, 7),
            "use_label_encoder": False,
            "eval_metric": "logloss",
            "random_state": random_state
        }
        
        clf = XGBClassifier(**params)
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)
        scores = cross_val_score(clf, X_train, y_train, cv=cv, scoring='roc_auc', n_jobs=-1)
        return scores.mean()

    study = optuna.create_study(direction="maximize")
    # Suppress verbose logging from optuna
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    study.optimize(objective, n_trials=n_trials)
    
    best_params = study.best_params
    best_params["use_label_encoder"] = False
    best_params["eval_metric"] = "logloss"
    best_params["random_state"] = random_state
    
    best_model = XGBClassifier(**best_params)
    best_model.fit(X_train, y_train)
    
    return best_model, study.best_params

def tune_lightgbm(X_train, y_train, random_state: int, n_trials: int) -> Tuple[Any, dict]:
    def objective(trial):
        params = {
            "n_estimators": trial.suggest_int("n_estimators", 50, 300),
            "max_depth": trial.suggest_int("max_depth", 3, 10),
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
            "subsample": trial.suggest_float("subsample", 0.6, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
            "random_state": random_state,
            "verbose": -1
        }
        clf = LGBMClassifier(**params)
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)
        scores = cross_val_score(clf, X_train, y_train, cv=cv, scoring='roc_auc', n_jobs=-1)
        return scores.mean()

    study = optuna.create_study(direction="maximize")
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    study.optimize(objective, n_trials=n_trials)
    
    best_params = study.best_params
    best_params["random_state"] = random_state
    best_params["verbose"] = -1
    
    best_model = LGBMClassifier(**best_params)
    best_model.fit(X_train, y_train)
    
    return best_model, study.best_params

def tune_model(model_name: str, X_train, y_train, random_state: int, n_trials: int) -> Tuple[Any, dict]:
    logger.info(f"Starting Hyperparameter Tuning for {model_name}...")
    if model_name == "XGBoost":
        return tune_xgboost(X_train, y_train, random_state, n_trials)
    elif model_name == "LightGBM":
        return tune_lightgbm(X_train, y_train, random_state, n_trials)
    else:
        # Fallback to XGBoost for others to keep it simple, or implement others as needed
        logger.warning(f"No specific tuner for {model_name}. Defaulting to XGBoost.")
        return tune_xgboost(X_train, y_train, random_state, n_trials)
