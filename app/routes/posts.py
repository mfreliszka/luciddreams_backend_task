"""Module containing add post endpoint."""

from fastapi import APIRouter, Depends, HTTPException
from app import schemas, models
from app.services import post_service
from app.database import get_db, get_current_user
import json
import redis
from sqlalchemy.orm import Session

router = APIRouter(prefix="")

# Initialize Redis client (assuming Redis is running locally on default port)
redis_client = redis.Redis(host="localhost", port=6379, db=0)

@router.post("/addpost", response_model=schemas.PostResponse)
def add_post(payload: schemas.PostCreate, 
             current_user: models.User = Depends(get_current_user), 
             db: Session = Depends(get_db)):
    """Create a new post for the authenticated user."""
    # The payload is already validated by Pydantic (including size limit).
    post = post_service.create_post(db, user_id=current_user.id, text=payload.text)
    # Invalidate cache for this user's posts, since data has changed
    cache_key = f"user:{current_user.id}:posts"
    redis_client.delete(cache_key)
    return post

@router.get("/getposts", response_model=list[schemas.PostResponse])
def get_posts(current_user: models.User = Depends(get_current_user), 
              db: Session = Depends(get_db)):
    """Retrieve all posts for the authenticated user, with caching."""
    cache_key = f"user:{current_user.id}:posts"
    # Check cache first
    cached = redis_client.get(cache_key)
    if cached:
        # Return cached data (it was stored as JSON)
        return json.loads(cached)
    # If not in cache, fetch from DB
    posts = post_service.get_posts(db, user_id=current_user.id)
    # Serialize posts via Pydantic model or manually for caching
    posts_data = [schemas.PostResponse.from_orm(p).dict() for p in posts]
    # Store in Redis with 5 minutes expiration
    redis_client.setex(cache_key, 300, json.dumps(posts_data))
    return posts_data

@router.delete("/deletepost")
def delete_post(post_id: int, 
                current_user: models.User = Depends(get_current_user), 
                db: Session = Depends(get_db)):
    """Delete a post by ID for the authenticated user."""
    success = post_service.delete_post(db, user_id=current_user.id, post_id=post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found or not owned by user")
    # Invalidate cache for user's posts
    redis_client.delete(f"user:{current_user.id}:posts")
    return {"detail": f"Post {post_id} deleted successfully."}
