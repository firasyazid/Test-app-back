from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal

class User(BaseModel):
    fullname: str
    email: EmailStr   
    password: str   
    role: Literal["doctor", "patient"]   
    created_at: Optional[datetime] = datetime.utcnow()
    updated_at: Optional[datetime] = datetime.utcnow()
