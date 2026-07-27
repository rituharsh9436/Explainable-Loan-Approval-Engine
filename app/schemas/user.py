from typing import Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[str] = "customer"
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    email: EmailStr
    password: str
    
class UserRead(UserBase):
    id: int
    
    class Config:
        from_attributes = True

class UserUpdate(UserBase):
    password: Optional[str] = None
