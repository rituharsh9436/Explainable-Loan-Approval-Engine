from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from app.schemas.prediction import (
    LoanApplication, 
    PredictionResponse, 
    ShapExplanationResponse, 
    LimeExplanationResponse,
    WhatIfSimulation,
    SimulationResponse
)
from app.services.prediction_service import PredictionService
from app.api.dependencies import get_prediction_service, get_current_active_user
from app.models.user import User
from app.core.config import settings

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
def predict_loan(
    data: LoanApplication,
    service: PredictionService = Depends(get_prediction_service),
    current_user: User = Depends(get_current_active_user)
):
    decision, prob = service.predict(data.model_dump())
    return PredictionResponse(decision=decision, approval_probability=prob)

@router.post("/explain/shap", response_model=ShapExplanationResponse)
def explain_shap(
    data: LoanApplication,
    service: PredictionService = Depends(get_prediction_service),
    current_user: User = Depends(get_current_active_user)
):
    base_value, shap_values = service.explain_shap(data.model_dump())
    return ShapExplanationResponse(base_value=base_value, shap_values=shap_values)

@router.post("/explain/lime")
def explain_lime(
    data: LoanApplication,
    service: PredictionService = Depends(get_prediction_service),
    current_user: User = Depends(get_current_active_user)
):
    return service.explain_lime(data.model_dump())

@router.get("/lime-report")
def lime_report():
    return FileResponse(
        str(settings.BASE_DIR / "lime_explanation.html"),
        media_type="text/html"
    )

@router.post("/simulate", response_model=SimulationResponse)
def simulate_what_if(
    sim: WhatIfSimulation,
    service: PredictionService = Depends(get_prediction_service),
    current_user: User = Depends(get_current_active_user)
):
    sim_params = {
        "new_applicant_income": sim.new_applicant_income,
        "new_loan_amount": sim.new_loan_amount,
        "new_loan_term": sim.new_loan_term
    }
    result = service.simulate(sim.base_application.model_dump(), sim_params)
    return SimulationResponse(**result)
