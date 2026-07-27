from pydantic import BaseModel, Field, model_validator
from typing import Literal, Optional

class LoanApplication(BaseModel):
    Gender: Literal["Male", "Female"]
    Married: Literal["Yes", "No"]
    Dependents: Literal["0", "1", "2", "3+"]
    Education: Literal["Graduate", "Not Graduate"]
    Employment_Status: Literal["Salaried", "Self-Employed", "Unemployed"]
    Applicant_Income: float = Field(..., ge=0)
    Coapplicant_Income: float = Field(..., ge=0)
    Loan_Amount: float = Field(..., gt=0)
    Loan_Term: float = Field(..., gt=0)
    Credit_History: Literal[0, 1]
    Property_Area: Literal["Rural", "Semiurban", "Urban"]
    Age: int = Field(..., ge=18, le=100)

    @model_validator(mode="after")
    def validate_total_income(self):
        if self.Applicant_Income + self.Coapplicant_Income <= 0:
            raise ValueError("Total income must be greater than zero")
        return self

class WhatIfSimulation(BaseModel):
    base_application: LoanApplication
    new_applicant_income: Optional[float] = Field(default=None, ge=0)
    new_loan_amount: Optional[float] = Field(default=None, gt=0)
    new_loan_term: Optional[float] = Field(default=None, gt=0)

class PredictionResponse(BaseModel):
    decision: str
    approval_probability: float

class ShapExplanationResponse(BaseModel):
    base_value: float
    shap_values: dict

class LimeExplanationResponse(BaseModel):
    lime_features: dict
    prediction_probabilities: dict

class SimulationResponse(BaseModel):
    original_probability: float
    new_probability: float
    original_decision: str
    new_decision: str
