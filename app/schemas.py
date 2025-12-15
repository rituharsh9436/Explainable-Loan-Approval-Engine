from pydantic import BaseModel
from typing import Optional

class LoanApplication(BaseModel):
    Gender: str
    Married: str
    Dependents: str
    Education: str
    Employment_Status: str
    Applicant_Income: float
    Coapplicant_Income: float
    Loan_Amount: float
    Loan_Term: float
    Credit_History: float
    Property_Area: str
    Age: int

class WhatIfSimulation(BaseModel):
    base_application: LoanApplication
    new_applicant_income: Optional[float] = None
    new_loan_amount: Optional[float] = None
    new_loan_term: Optional[float] = None
