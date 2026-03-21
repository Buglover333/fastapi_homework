from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional
from api.database import register_user, login_user

auth_router = APIRouter(prefix="/auth", tags=["authentication"])

class LoginRequest(BaseModel):
    username_or_email: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    user: Optional[dict] = None

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class RegisterResponse(BaseModel):
    success: bool
    message: str
    user: Optional[dict] = None

@auth_router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest):
    user, message = login_user(login_data.username_or_email, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message
        )
    
    return LoginResponse(
        success=True,
        message=message,
        user=user
    )

@auth_router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(register_data: RegisterRequest):
    user, message = register_user(
        username=register_data.username,
        email=register_data.email,
        password=register_data.password,
        full_name=register_data.full_name
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    
    return RegisterResponse(
        success=True,
        message=message,
        user=user
    )