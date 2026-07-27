from sqlalchemy.orm import Session
from app.repositories.base import CRUDBase
from app.models.loan_application import LoanApplication

class CRUDLoanApplication(CRUDBase[LoanApplication]):
    pass

loan_application = CRUDLoanApplication(LoanApplication)
