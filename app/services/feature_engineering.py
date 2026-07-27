import pandas as pd
from typing import Dict, Any, List
from app.core.exceptions import FeatureEngineeringError

def preprocess_input(data: Dict[str, Any], feature_columns: List[str]) -> pd.DataFrame:
    try:
        df = pd.DataFrame([data])
        
        df['Total_Income'] = df['Applicant_Income'] + df['Coapplicant_Income']
        if (df['Total_Income'] <= 0).any():
            raise ValueError("Total income must be greater than zero.")

        df['Loan_to_Income_Ratio'] = df['Loan_Amount'] / df['Total_Income']
        df = pd.get_dummies(df)
        df = df.reindex(columns=feature_columns, fill_value=0)
        
        return df
    except Exception as e:
        raise FeatureEngineeringError(f"Failed to engineer features: {str(e)}")
