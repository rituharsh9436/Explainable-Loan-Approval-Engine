import os
import json
import joblib
import logging
from datetime import datetime
from typing import Dict, Any
from .config import MODEL_PATH, PREPROCESSOR_PATH, FEATURE_COLS_PATH, METADATA_PATH, MODEL_VERSION, MODELS_DIR

logger = logging.getLogger(__name__)

def save_artifacts(
    model: Any, 
    preprocessor: Any, 
    feature_columns: list, 
    metrics: Dict[str, Any],
    best_params: Dict[str, Any],
    dataset_size: int,
    algorithm: str
):
    """
    Serializes all required artifacts for production deployment.
    """
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    # Save Model
    joblib.dump(model, MODEL_PATH)
    logger.info(f"Saved model to {MODEL_PATH}")
    
    # Save Preprocessor Pipeline
    joblib.dump(preprocessor, PREPROCESSOR_PATH)
    logger.info(f"Saved preprocessor to {PREPROCESSOR_PATH}")
    
    # Save Feature Columns (needed to ensure dataframe matches expected shape before prediction)
    joblib.dump(feature_columns, FEATURE_COLS_PATH)
    logger.info(f"Saved feature columns to {FEATURE_COLS_PATH}")
    
    # Generate and Save Metadata
    metadata = {
        "version": MODEL_VERSION,
        "algorithm": algorithm,
        "training_date": datetime.utcnow().isoformat() + "Z",
        "dataset_size": dataset_size,
        "best_parameters": best_params,
        "metrics": metrics
    }
    
    with open(METADATA_PATH, "w") as f:
        json.dump(metadata, f, indent=4)
        
    logger.info(f"Saved metadata to {METADATA_PATH}")
