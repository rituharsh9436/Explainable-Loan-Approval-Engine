from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class LoanApplication(Base):
    __tablename__ = "loan_applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Optional for now
    
    # Applicant details
    gender = Column(String)
    married = Column(String)
    dependents = Column(String)
    education = Column(String)
    employment_status = Column(String)
    applicant_income = Column(Float)
    coapplicant_income = Column(Float)
    
    # Loan details
    loan_amount = Column(Float)
    loan_term = Column(Float)
    credit_history = Column(Integer)
    property_area = Column(String)
    age = Column(Integer)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    predictions = relationship("Prediction", back_populates="application", cascade="all, delete-orphan")
