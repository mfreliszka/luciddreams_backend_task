"""Module containing auth endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas
from app.services import auth_service, user_service
from app.database import get_db

router = APIRouter(prefix="")

@router.post("/signup", response_model=schemas.TokenResponse)
def signup(user_data: schemas.UserSignup, db: Session = Depends(get_db)):
    """User registration endpoint: creates a new user and returns a JWT token."""
    # Check if email already registered
    if user_service.get_user_by_email(db, user_data.email):
        raise HTTPException(status_code=400, detail="Email is already registered")
    # Hash the password and create user
    hashed_pw = auth_service.hash_password(user_data.password)
    user = user_service.create_user(db, email=user_data.email, password_hash=hashed_pw)
    # Generate a JWT token for the new user
    access_token = auth_service.create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=schemas.TokenResponse)
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    """User login endpoint: verifies credentials and returns a JWT token."""
    user = user_service.get_user_by_email(db, credentials.email)
    if not user or not auth_service.verify_password(credentials.password, user.password_hash):
        # Authentication failed
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    # Credentials are valid, create JWT
    access_token = auth_service.create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
