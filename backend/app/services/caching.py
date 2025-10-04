# Redis caching utilities
import redis
from ..config import settings

r = redis.from_url(settings.REDIS_URL)

def cache_key(prefix: str, **kwargs) -> str:
    parts = [prefix] + [f"{k}={v}" for k, v in sorted(kwargs.items()) if v is not None]
    return ":".join(parts)
