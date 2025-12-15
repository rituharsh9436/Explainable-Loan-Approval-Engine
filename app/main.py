#Harsh Bhardwaj
from fastapi import FastAPI
import joblib
import shap
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import LoanApplication, WhatIfSimulation
from app.utils import preprocess_input

app = FastAPI(title="Explainable Loan Approval Engine")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model & artifacts
model = joblib.load("models/xgboost_loan_model.pkl")
explainer = joblib.load("models/shap_explainer.pkl")
feature_columns = joblib.load("models/feature_columns.pkl")

@app.get("/")
def home():
    return {"message": "Explainable Loan Approval Engine is running"}

@app.post("/predict")
def predict_loan(data: LoanApplication):
    X = preprocess_input(data.dict(), feature_columns)
    prob = model.predict_proba(X)[0][1]
    decision = "Approved" if prob >= 0.65 else "Rejected"


    return {
        "decision": decision,
        "approval_probability": round(float(prob), 3)
    }

@app.post("/explain/shap")
def explain_shap(data: LoanApplication):
    X = preprocess_input(data.dict(), feature_columns)
    shap_values = explainer.shap_values(X)

    explanation = dict(zip(
        X.columns,
        shap_values[0].tolist()
    ))

    return {
        "base_value": explainer.expected_value,
        "shap_values": explanation
    }
@app.post("/simulate")
def simulate_what_if(sim: WhatIfSimulation):
    base_data = sim.base_application.dict()

    # Original prediction
    X_orig = preprocess_input(base_data, feature_columns)
    orig_prob = model.predict_proba(X_orig)[0][1]

    # Apply changes
    if sim.new_applicant_income is not None:
        base_data['Applicant_Income'] = sim.new_applicant_income

    if sim.new_loan_amount is not None:
        base_data['Loan_Amount'] = sim.new_loan_amount

    if sim.new_loan_term is not None:
        base_data['Loan_Term'] = sim.new_loan_term

    # New prediction
    X_new = preprocess_input(base_data, feature_columns)
    new_prob = model.predict_proba(X_new)[0][1]

    return {
        "original_probability": round(float(orig_prob), 3),
        "new_probability": round(float(new_prob), 3),
        "original_decision": "Approved" if orig_prob >= 0.5 else "Rejected",
        "new_decision": "Approved" if new_prob >= 0.5 else "Rejected"
    }
