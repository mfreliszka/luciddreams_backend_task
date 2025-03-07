"""Module containing database models."""
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    """Database model for users."""
    
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)  # store bcrypt hash
    posts = relationship("Post", back_populates="owner")

class Post(Base):
    """Database model for posts."""
    
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="posts")
