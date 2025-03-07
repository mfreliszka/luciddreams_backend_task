"""Module containing redis settings."""

import redis
from app.settings import settings

redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)

def cache_set(key: str, value: str, expiration: int = 300):
    """Set a value in Redis with an expiration time (default 5 minutes)."""
    redis_client.setex(key, expiration, value)

def cache_get(key: str):
    """Retrieve a cached value from Redis."""
    return redis_client.get(key)

def cache_delete(key: str):
    """Delete a cache key."""
    redis_client.delete(key)
