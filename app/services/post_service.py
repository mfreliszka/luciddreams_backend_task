"""Module containing post service."""

from sqlalchemy.orm import Session
from app import models

def create_post(db: Session, user_id: int, text: str) -> models.Post:
    """Create a new post for a given user and return the Post object."""
    post = models.Post(text=text, owner_id=user_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def get_posts(db: Session, user_id: int) -> list[models.Post]:
    """Retrieve all posts for the given user."""
    return db.query(models.Post).filter(models.Post.owner_id == user_id).all()

def delete_post(db: Session, user_id: int, post_id: int) -> bool:
    """Delete a post by ID if it belongs to the given user. Returns True if deleted."""
    post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.owner_id == user_id).first()
    if post:
        db.delete(post)
        db.commit()
        return True
    return False
