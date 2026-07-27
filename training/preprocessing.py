from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from .config import CATEGORICAL_COLS, NUMERICAL_COLS
from .feature_engineering import FeatureEngineer

def get_preprocessor() -> Pipeline:
    """
    Creates a scikit-learn Pipeline that handles missing values, 
    encodes categorical variables, scales numerical features, 
    and applies our custom feature engineering.
    """
    
    # We will build a pipeline where FeatureEngineer runs first on raw data,
    # then we update the numeric columns list dynamically to include the new features.
    
    # Actually, if FeatureEngineer runs first, it will produce new columns. 
    # The ColumnTransformer needs to know about these new columns.
    
    new_numerical_cols = NUMERICAL_COLS + [
        "total_assets",
        "loan_to_income_ratio",
        "assets_to_loan_ratio",
        "emi_proxy",
        "emi_to_income_ratio"
    ]
    
    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        # handle_unknown="ignore" prevents crashes if a new category appears in production
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, new_numerical_cols),
            ("cat", categorical_transformer, CATEGORICAL_COLS)
        ]
    )

    # The full pipeline: engineer features first, then transform
    full_pipeline = Pipeline(steps=[
        ("feature_engineering", FeatureEngineer()),
        ("preprocessor", preprocessor)
    ])
    
    return full_pipeline
