import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "loan_approval_dataset.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Versioning
MODEL_VERSION = "v2"

# File output paths
MODEL_PATH = os.path.join(MODELS_DIR, f"loan_model_{MODEL_VERSION}.pkl")
PREPROCESSOR_PATH = os.path.join(MODELS_DIR, f"preprocessing_{MODEL_VERSION}.pkl")
FEATURE_COLS_PATH = os.path.join(MODELS_DIR, f"feature_columns_{MODEL_VERSION}.pkl")
METADATA_PATH = os.path.join(MODELS_DIR, f"metadata_{MODEL_VERSION}.json")

# Target and features
TARGET_COL = "loan_status"
# Based on the dataset exploration, we have these exact column names. Note: dataset has leading spaces in headers sometimes.
# We will strip them during data loading.
CATEGORICAL_COLS = ["education", "self_employed"]
NUMERICAL_COLS = [
    "no_of_dependents", 
    "income_annum", 
    "loan_amount", 
    "loan_term", 
    "cibil_score", 
    "residential_assets_value", 
    "commercial_assets_value", 
    "luxury_assets_value", 
    "bank_asset_value"
]

# Random Seed for reproducibility
RANDOM_STATE = 42

# Optuna configuration
OPTUNA_TRIALS = 30  # Adjust based on time constraints. 30 is decent for an MVP.
