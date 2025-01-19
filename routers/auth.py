from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from db import user_collection, create_user, get_user_by_email
from pydantic import BaseModel, EmailStr
from datetime import datetime
from utils.jwt_handler import create_access_token, decode_access_token
from typing import Optional, Literal

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    fullname: str
    email: EmailStr  
    password: str  
    role: Literal["doctor", "patient"] 
    created_at: Optional[datetime] = datetime.utcnow()
    updated_at: Optional[datetime] = datetime.utcnow()

class Login(BaseModel):
    email: EmailStr  
    password: str  


# Register 
@router.post("/register", tags=["Authentication"])
def register(user: User):
    if get_user_by_email(user_collection, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user_data = user.dict()
    user_data["password"] = pwd_context.hash(user.password)  
    user_data["created_at"] = datetime.utcnow()
    user_data["updated_at"] = datetime.utcnow()

    user_id = create_user(user_collection, user_data)

    return {"message": "User registered successfully", "user_id": user_id}


# Login 
@router.post("/login", tags=["Authentication"])
def login(login_data: Login):
    user = get_user_by_email(user_collection, login_data.email)
    if not user or not pwd_context.verify(login_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"email": user["email"], "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}


# Get all
@router.get("/users", tags=["Users"])
def get_all_users():
    users = user_collection.find()
    user_list = []
    for user in users:
        user["_id"] = str(user["_id"])   
        user.pop("password", None)   
        user_list.append(user)
    return user_list


 
@router.get("/me", tags=["Authentication"])
def get_me(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return {"email": payload["email"], "role": payload["role"]}
