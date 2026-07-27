import pandas as pd
import joblib
from typing import Dict, Any, List
from app.core.exceptions import FeatureEngineeringError
from app.core.config import settings

# Load the new preprocessor lazily or globally
preprocessor = None

def get_preprocessor():
    global preprocessor
    if preprocessor is None:
        preprocessor = joblib.load(settings.MODELS_DIR / "preprocessing_v2.pkl")
    return preprocessor

def preprocess_input(data: Dict[str, Any], feature_columns: List[str]) -> pd.DataFrame:
    try:
        # 1. Map old API schema (LoanApplication) to the new Model Schema (loan_approval_dataset)
        
        # Parse dependents
        deps_str = str(data.get("Dependents", "0")).replace("+", "")
        no_of_dependents = int(deps_str) if deps_str.isdigit() else 0
        
        # Education mapping (matches exactly "Graduate", "Not Graduate")
        education = data.get("Education", "Graduate")
        
        # Employment mapping
        self_employed = "Yes" if data.get("Employment_Status") == "Self-Employed" else "No"
        
        # Income mapping
        income_annum = float(data.get("Applicant_Income", 0)) + float(data.get("Coapplicant_Income", 0))
        
        # CIBIL Score mapping (Credit_History is 1 or 0)
        cibil_score = 750 if data.get("Credit_History", 1) == 1 else 300
        
        mapped_data = {
            "no_of_dependents": no_of_dependents,
            "education": education,
            "self_employed": self_employed,
            "income_annum": income_annum,
            "loan_amount": float(data.get("Loan_Amount", 0)),
            "loan_term": float(data.get("Loan_Term", 12)),
            "cibil_score": cibil_score,
            # Assigning 0 or reasonable defaults for missing asset data from old API
            "residential_assets_value": 0,
            "commercial_assets_value": 0,
            "luxury_assets_value": 0,
            "bank_asset_value": income_annum * 0.2  # arbitrary 20% of income as bank asset
        }
        
        df_raw = pd.DataFrame([mapped_data])
        
        # 2. Run the trained preprocessor pipeline (v2)
        prep = get_preprocessor()
        processed_array = prep.transform(df_raw)
        
        # 3. Return a DataFrame with the exact feature columns the XGBoost model expects
        df_final = pd.DataFrame(processed_array, columns=feature_columns)
        
        return df_final
    except Exception as e:
        raise FeatureEngineeringError(f"Failed to engineer features: {str(e)}")
