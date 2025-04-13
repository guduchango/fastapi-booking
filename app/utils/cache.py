from typing import Any, Optional
import json
from redis import Redis
import os
from functools import wraps

# Initialize Redis client
redis_client = Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    db=0,
    decode_responses=True
)

def cache_key(prefix: str, *args, **kwargs) -> str:
    """Generate a cache key from function arguments."""
    key_parts = [prefix]
    key_parts.extend(str(arg) for arg in args)
    key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
    return ":".join(key_parts)

def cached(ttl: int = 300):
    """Decorator to cache function results in Redis."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            key = cache_key(func.__name__, *args, **kwargs)
            
            # Try to get from cache
            cached_value = redis_client.get(key)
            if cached_value is not None:
                return json.loads(cached_value)
            
            # Execute function if not in cache
            result = await func(*args, **kwargs)
            
            # Store in cache
            redis_client.setex(key, ttl, json.dumps(result))
            
            return result
        return wrapper
    return decorator

def invalidate_cache(prefix: str):
    """Decorator to invalidate cache entries matching a prefix."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Execute the function
            result = await func(*args, **kwargs)
            
            # Invalidate cache
            pattern = f"{prefix}:*"
            keys = redis_client.keys(pattern)
            if keys:
                redis_client.delete(*keys)
            
            return result
        return wrapper
    return decorator 