import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class FeatureEngineer(BaseEstimator, TransformerMixin):
    """
    Scikit-learn compatible transformer for custom feature engineering.
    This allows us to seamlessly integrate it into the preprocessing Pipeline.
    """
    def __init__(self):
        pass
        
    def fit(self, X: pd.DataFrame, y=None):
        return self
        
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X_out = X.copy()
        
        # Total Assets
        asset_cols = [
            "residential_assets_value", 
            "commercial_assets_value", 
            "luxury_assets_value", 
            "bank_asset_value"
        ]
        X_out["total_assets"] = X_out[asset_cols].sum(axis=1)
        
        # Loan to Income Ratio
        # Small epsilon to avoid division by zero just in case
        X_out["loan_to_income_ratio"] = X_out["loan_amount"] / (X_out["income_annum"] + 1e-5)
        
        # Total Assets to Loan Ratio
        X_out["assets_to_loan_ratio"] = X_out["total_assets"] / (X_out["loan_amount"] + 1e-5)
        
        # Monthly EMI proxy (assuming 10% interest roughly for the whole term just as a raw feature)
        # term is in years usually, so term * 12 months.
        term_months = X_out["loan_term"] * 12
        X_out["emi_proxy"] = (X_out["loan_amount"] * 1.10) / (term_months + 1e-5)
        
        # EMI to Income ratio
        X_out["emi_to_income_ratio"] = X_out["emi_proxy"] / ((X_out["income_annum"] / 12) + 1e-5)
        
        return X_out
