import pandas as pd
from typing import Tuple
from .config import DATA_PATH, TARGET_COL

def load_data() -> Tuple[pd.DataFrame, pd.Series]:
    """
    Loads the dataset and performs initial sanitization (stripping spaces from column names and string values).
    """
    df = pd.read_csv(DATA_PATH)
    
    # The dataset has spaces in column names like " loan_status"
    df.columns = df.columns.str.strip()
    
    # The categorical values also have leading spaces like " Approved"
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()
    
    # We drop loan_id as it has no predictive power
    if "loan_id" in df.columns:
        df = df.drop(columns=["loan_id"])
        
    X = df.drop(columns=[TARGET_COL])
    
    # Map target to 1 (Approved) and 0 (Rejected)
    # Checking values to ensure we map properly
    y = df[TARGET_COL].map({"Approved": 1, "Rejected": 0})
    
    return X, y
