"""Module containing user service."""

from sqlalchemy.orm import Session
from app import models

def get_user_by_email(db: Session, email: str):
    """Fetch a user by email."""
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, email: str, password_hash: str):
    """Create a new user in the database."""
    user = models.User(email=email, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
