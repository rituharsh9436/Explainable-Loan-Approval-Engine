from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("loan_applications.id"))
    model_version_id = Column(Integer, ForeignKey("model_versions.id"), nullable=True)
    
    decision = Column(String, nullable=False) # Approved or Rejected
    approval_probability = Column(Float, nullable=False)
    
    # JSONB is great for storing variable schema outputs like SHAP/LIME
    # In SQLite it falls back to simple text JSON
    explanation_shap = Column(JSON, nullable=True)
    explanation_lime = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    application = relationship("LoanApplication", back_populates="predictions")
    model_version = relationship("ModelVersion")
