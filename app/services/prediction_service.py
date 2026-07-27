import numpy as np
import pandas as pd
import time
import structlog
from typing import Dict, Any, Tuple
from app.core.config import settings
from app.services.model_repository import ModelRepository
from app.services.feature_engineering import preprocess_input
from app.core.exceptions import PredictionError

logger = structlog.get_logger(__name__)

class PredictionService:
    def __init__(self, model_repo: ModelRepository):
        self.repo = model_repo
        self.model = self.repo.get_model()
        self.feature_columns = self.repo.get_feature_columns()

    def _decision_from_probability(self, probability: float) -> str:
        return "Approved" if probability >= settings.APPROVAL_THRESHOLD else "Rejected"

    def predict(self, application_data: Dict[str, Any]) -> Tuple[str, float]:
        start_time = time.perf_counter()
        try:
            X = preprocess_input(application_data, self.feature_columns)
            prob = self.model.predict_proba(X)[0][1]
            decision = self._decision_from_probability(prob)
            
            inference_time_ms = (time.perf_counter() - start_time) * 1000
            
            logger.info("prediction_completed", 
                        decision=decision, 
                        probability=round(float(prob), 3), 
                        inference_time_ms=round(inference_time_ms, 2),
                        inputs=application_data)
            
            return decision, round(float(prob), 3)
        except Exception as e:
            logger.error("prediction_failed", error=str(e), inputs=application_data)
            raise PredictionError(f"Prediction failed: {str(e)}")

    def explain_shap(self, application_data: Dict[str, Any]) -> Tuple[float, Dict[str, float]]:
        try:
            X = preprocess_input(application_data, self.feature_columns)
            explainer = self.repo.get_shap_explainer()
            shap_values = explainer.shap_values(X)
            
            # Extract class 1 values
            if isinstance(shap_values, list):
                val = shap_values[1] if len(shap_values) > 1 else shap_values[0]
            else:
                val = shap_values
                
            val_array = np.asarray(val)
            if val_array.ndim == 3:
                val_array = val_array[:, :, 1]
            feature_values = val_array[0].astype(float).tolist()
            
            explanation = dict(zip(X.columns, feature_values))
            
            # Base value
            base_val_array = np.asarray(explainer.expected_value).ravel()
            base_value = float(base_val_array[1]) if base_val_array.size > 1 else float(base_val_array[0])
            
            return base_value, explanation
        except Exception as e:
            raise PredictionError(f"SHAP explanation failed: {str(e)}")

    def explain_lime(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        lime_explainer = self.repo.get_lime_explainer()
        if lime_explainer is None:
            return {"type": "html_report", "url": "/lime-report"}
            
        try:
            X = preprocess_input(application_data, self.feature_columns)
            lime_exp = lime_explainer.explain_instance(
                data_row=X.iloc[0].values,
                predict_fn=self.model.predict_proba,
                num_features=10
            )
            lime_features = dict(lime_exp.as_list())
            
            return {
                "lime_features": lime_features,
                "prediction_probabilities": {
                    "Rejected": float(self.model.predict_proba(X)[0][0]),
                    "Approved": float(self.model.predict_proba(X)[0][1])
                }
            }
        except Exception as e:
            raise PredictionError(f"LIME explanation failed: {str(e)}")
            
    def simulate(self, base_data: Dict[str, Any], sim_params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            X_orig = preprocess_input(base_data, self.feature_columns)
            orig_prob = self.model.predict_proba(X_orig)[0][1]
            
            # Apply changes
            modified_data = base_data.copy()
            if sim_params.get("new_applicant_income") is not None:
                modified_data['Applicant_Income'] = sim_params["new_applicant_income"]
            if sim_params.get("new_loan_amount") is not None:
                modified_data['Loan_Amount'] = sim_params["new_loan_amount"]
            if sim_params.get("new_loan_term") is not None:
                modified_data['Loan_Term'] = sim_params["new_loan_term"]
                
            X_new = preprocess_input(modified_data, self.feature_columns)
            new_prob = self.model.predict_proba(X_new)[0][1]
            
            return {
                "original_probability": round(float(orig_prob), 3),
                "new_probability": round(float(new_prob), 3),
                "original_decision": self._decision_from_probability(orig_prob),
                "new_decision": self._decision_from_probability(new_prob)
            }
        except Exception as e:
            raise PredictionError(f"Simulation failed: {str(e)}")
