"""Module containing database settings."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from app.settings import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import auth_service, user_service


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
Base = declarative_base()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Dependency to get the current user from the JWT token, or raise if invalid."""
    payload = auth_service.decode_access_token(token)
    if payload is None or "sub" not in payload:
        # Invalid token or expired
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})
    user_email = payload["sub"]
    user = user_service.get_user_by_email(db, user_email)  # function to get user from DB
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    return user