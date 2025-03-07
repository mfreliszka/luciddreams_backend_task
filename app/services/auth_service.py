"""Module containing auth service."""

from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "SUPERSECRETJWTKEY"            # load from config in real use
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60           # e.g., 60 minutes token expiry

def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against the stored hash."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    """Generate a JWT token with an expiration."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    """Decode a JWT token. Returns the payload if valid, else None."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # payload will contain our data (e.g. email)
    except jwt.ExpiredSignatureError:
        return None  # token expired
    except jwt.PyJWTError:
        return None  # token invalid
