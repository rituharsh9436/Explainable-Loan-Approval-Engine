import logging
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.repositories.user_repo import user as user_repo
from app.core.security import get_password_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db(db: Session) -> None:
    admin_email = "admin@example.com"
    user = user_repo.get_by_email(db, email=admin_email)
    
    if not user:
        user_in = {
            "email": admin_email,
            "hashed_password": get_password_hash("admin123"), # Hardcoded for demo/seed
            "full_name": "System Admin",
            "role": "admin",
            "is_active": True
        }
        user = user_repo.create(db, obj_in=user_in)
        logger.info(f"Created seed admin user: {admin_email}")
    else:
        logger.info(f"Admin user {admin_email} already exists.")

if __name__ == "__main__":
    logger.info("Creating initial data")
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()
    logger.info("Initial data created")
