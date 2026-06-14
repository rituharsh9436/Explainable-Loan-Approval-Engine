import pickle
from pathlib import Path
from fastapi.responses import FileResponse
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np
import shap

from app.schemas import LoanApplication, WhatIfSimulation
from app.utils import preprocess_input

APPROVAL_THRESHOLD = 0.65
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"

app = FastAPI(title="Explainable Loan Approval Engine")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model & artifacts
model = joblib.load(MODELS_DIR / "xgboost_loan_model.pkl")
shap_explainer = joblib.load(MODELS_DIR / "shap_explainer.pkl")
feature_columns = joblib.load(MODELS_DIR / "feature_columns.pkl")

# Load LIME explainer (optional)
lime_explainer = None
try:
    with open(MODELS_DIR / "lime_explainer.pkl", "rb") as f:
        lime_explainer = pickle.load(f)
except FileNotFoundError:
    pass
    # print("WARNING: lime_explainer.pkl not found. Run the notebook to generate it.")

def application_dict(data: LoanApplication):
    if hasattr(data, "model_dump"):
        return data.model_dump()
    return data.dict()

def decision_from_probability(probability):
    return "Approved" if probability >= APPROVAL_THRESHOLD else "Rejected"

def build_features(data):
    try:
        return preprocess_input(data, feature_columns)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

def class_one_values(values):
    if isinstance(values, list):
        values = values[1] if len(values) > 1 else values[0]

    values_array = np.asarray(values)
    if values_array.ndim == 3:
        values_array = values_array[:, :, 1]

    return values_array[0].astype(float).tolist()

def class_one_base_value(value):
    value_array = np.asarray(value).ravel()
    if value_array.size > 1:
        return float(value_array[1])
    return float(value_array[0])

@app.get("/")
def home():
    return {"message": "Explainable Loan Approval Engine is running"}

@app.post("/predict")
def predict_loan(data: LoanApplication):
    X = build_features(application_dict(data))
    prob = model.predict_proba(X)[0][1]
    decision = decision_from_probability(prob)


    return {
        "decision": decision,
        "approval_probability": round(float(prob), 3)
    }

@app.post("/explain/shap")
def explain_shap(data: LoanApplication):
    X = build_features(application_dict(data))
    shap_values = shap_explainer.shap_values(X)
    feature_values = class_one_values(shap_values)

    explanation = dict(zip(
        X.columns,
        feature_values
    ))

    return {
        "base_value": class_one_base_value(shap_explainer.expected_value),
        "shap_values": explanation
    }

@app.get("/lime-report")
def lime_report():
    return FileResponse(
        str(BASE_DIR / "lime_explanation.html"),
        media_type="text/html"
    )

@app.post("/explain/lime")
def explain_lime(data: LoanApplication):
    if lime_explainer is None:
        return {
            "type": "html_report",
            "url": "/lime-report"
        }
    
    X = build_features(application_dict(data))
    lime_exp = lime_explainer.explain_instance(
        data_row=X.iloc[0].values,
        predict_fn=model.predict_proba,
        num_features=10
    )
    
    # Extract feature contributions
    lime_features = dict(lime_exp.as_list())
    
    return {
        "lime_features": jsonable_encoder(lime_features),
        "prediction_probabilities": {
            "Rejected": float(model.predict_proba(X)[0][0]),
            "Approved": float(model.predict_proba(X)[0][1])
        }
    }
@app.post("/simulate")
def simulate_what_if(sim: WhatIfSimulation):
    base_data = application_dict(sim.base_application)

    # Original prediction
    X_orig = build_features(base_data)
    orig_prob = model.predict_proba(X_orig)[0][1]

    # Apply changes
    if sim.new_applicant_income is not None:
        base_data['Applicant_Income'] = sim.new_applicant_income

    if sim.new_loan_amount is not None:
        base_data['Loan_Amount'] = sim.new_loan_amount

    if sim.new_loan_term is not None:
        base_data['Loan_Term'] = sim.new_loan_term

    # New prediction
    X_new = build_features(base_data)
    new_prob = model.predict_proba(X_new)[0][1]

    return {
        "original_probability": round(float(orig_prob), 3),
        "new_probability": round(float(new_prob), 3),
        "original_decision": decision_from_probability(orig_prob),
        "new_decision": decision_from_probability(new_prob)
    }
