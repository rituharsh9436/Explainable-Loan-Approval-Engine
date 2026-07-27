import joblib
import pickle
import logging
from typing import Any, List, Optional
from app.core.config import settings
from app.core.exceptions import ModelLoadError

logger = logging.getLogger(__name__)

class ModelRepository:
    """
    Singleton repository to manage loading and caching of ML models.
    Prevents repeated disk I/O and keeps the model in memory.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelRepository, cls).__new__(cls)
            cls._instance._load_models()
        return cls._instance

    def _load_models(self):
        try:
            self.model = joblib.load(settings.MODELS_DIR / "xgboost_loan_model.pkl")
            self.shap_explainer = joblib.load(settings.MODELS_DIR / "shap_explainer.pkl")
            self.feature_columns = joblib.load(settings.MODELS_DIR / "feature_columns.pkl")
            
            # LIME is optional
            self.lime_explainer = None
            try:
                with open(settings.MODELS_DIR / "lime_explainer.pkl", "rb") as f:
                    self.lime_explainer = pickle.load(f)
            except FileNotFoundError:
                logger.warning("LIME explainer not found. LIME explanations will rely on HTML report fallback.")
                
        except Exception as e:
            logger.error(f"Failed to load ML models: {e}")
            raise ModelLoadError("Could not initialize ML models.")

    def get_model(self) -> Any:
        return self.model
        
    def get_shap_explainer(self) -> Any:
        return self.shap_explainer
        
    def get_lime_explainer(self) -> Optional[Any]:
        return self.lime_explainer
        
    def get_feature_columns(self) -> List[str]:
        return self.feature_columns
