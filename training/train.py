import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

from .config import RANDOM_STATE, OPTUNA_TRIALS
from .data_loader import load_data
from .preprocessing import get_preprocessor
from .model_selection import evaluate_baselines
from .hyperparameter_tuning import tune_model
from .explainability import evaluate_model, check_shap_compatibility
from .save_model import save_artifacts

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting MLOps Retraining Pipeline...")
    
    # 1. Load Data
    X, y = load_data()
    dataset_size = len(X)
    logger.info(f"Loaded dataset: {dataset_size} rows")
    
    # 2. Train/Test Split
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )
    
    # 3. Preprocessing & Feature Engineering
    logger.info("Applying preprocessing and feature engineering...")
    preprocessor = get_preprocessor()
    
    # Fit on training data and transform both
    X_train_processed = preprocessor.fit_transform(X_train_raw)
    X_test_processed = preprocessor.transform(X_test_raw)
    
    # Extract final feature column names from the pipeline
    # We must construct this dynamically or fetch it from the transformers if we want exact names
    try:
        # scikit-learn >= 1.0 supports get_feature_names_out directly on ColumnTransformer
        feature_columns = preprocessor.named_steps["preprocessor"].get_feature_names_out().tolist()
    except Exception as e:
        logger.warning(f"Could not extract feature names dynamically: {e}. Will rely on raw shapes.")
        # Fallback to generic names if it fails
        feature_columns = [f"f_{i}" for i in range(X_train_processed.shape[1])]
    
    # Convert back to dataframe for tree models and SHAP
    X_train_df = pd.DataFrame(X_train_processed, columns=feature_columns)
    X_test_df = pd.DataFrame(X_test_processed, columns=feature_columns)
    
    # 4. Handle Class Imbalance using SMOTE
    logger.info("Applying SMOTE to training data to handle class imbalance...")
    smote = SMOTE(random_state=RANDOM_STATE)
    X_train_balanced, y_train_balanced = smote.fit_resample(X_train_df, y_train)
    logger.info(f"Training data shape after SMOTE: {X_train_balanced.shape}")
    
    # 5. Baseline Evaluation
    logger.info("Evaluating baseline algorithms...")
    baseline_results = evaluate_baselines(X_train_balanced, y_train_balanced, RANDOM_STATE)
    logger.info(f"Baseline Results:\n{baseline_results.to_string(index=False)}")
    
    # Extract best model name
    best_model_name = baseline_results.iloc[0]["Model"]
    logger.info(f"Best baseline model is {best_model_name}. Proceeding to Hyperparameter Tuning.")
    
    # 6. Hyperparameter Tuning
    best_model, best_params = tune_model(
        best_model_name, X_train_balanced, y_train_balanced, RANDOM_STATE, OPTUNA_TRIALS
    )
    
    # 7. Final Evaluation on Holdout Test Set
    logger.info("Evaluating tuned model on test set...")
    metrics = evaluate_model(best_model, X_test_df, y_test)
    
    # 8. Sanity check Explainability
    check_shap_compatibility(best_model, X_test_df)
    
    # 9. Save Artifacts for Production
    logger.info("Saving artifacts for production deployment...")
    save_artifacts(
        model=best_model,
        preprocessor=preprocessor,
        feature_columns=feature_columns,
        metrics=metrics,
        best_params=best_params,
        dataset_size=dataset_size,
        algorithm=best_model_name
    )
    
    logger.info("MLOps Retraining Pipeline completed successfully!")

if __name__ == "__main__":
    main()
