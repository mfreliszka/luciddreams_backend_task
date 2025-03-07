"""Module containing app models."""
"""Module containing auth service."""
from pydantic import BaseModel, EmailStr, SecretStr, field_validator

class UserSignup(BaseModel):
    """Schema for user signup data."""
    
    email: EmailStr
    password: SecretStr

class UserLogin(BaseModel):
    """Schema for user login data."""
    
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    """Schema for token response data."""
    
    access_token: str
    token_type: str = "bearer"

class PostCreate(BaseModel):
    """Schema for creating a new post."""
    
    text: str

    # Validate that text payload is not larger than 1 MB (1048576 bytes)
    @field_validator('text')
    @classmethod
    def text_size_limit(cls, v):
        if len(v.encode('utf-8')) > 1024 * 1024:
            raise ValueError("Post text exceeds 1 MB size limit")
        return v

class PostResponse(BaseModel):
    """Schema for post response data."""
    
    id: int
    text: str

    class Config:
        orm_mode = True
