from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base_class import Base

class ModelVersion(Base):
    __tablename__ = "model_versions"

    id = Column(Integer, primary_key=True, index=True)
    version_tag = Column(String, unique=True, index=True, nullable=False)
    algorithm = Column(String, nullable=False) # e.g., 'xgboost'
    file_path = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    metrics_json = Column(String, nullable=True) # Could be JSON if using Postgres
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
