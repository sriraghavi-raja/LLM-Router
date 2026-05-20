from typing import AsyncGenerator
import redis.asyncio as aioredis
from app.config import get_settings
 
_redis_pool: aioredis.Redis | None = None
 
 
async def get_redis() -> AsyncGenerator[aioredis.Redis, None]:
    """FastAPI dependency — yields an async Redis connection."""
    global _redis_pool
    if _redis_pool is None:
        settings = get_settings()
        _redis_pool = aioredis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=False,  # Raw bytes for embeddings
        )
    yield _redis_pool
 
 
async def health_check() -> bool:
    """Ping Redis. Returns True if reachable."""
    try:
        settings = get_settings()
        r = aioredis.from_url(settings.redis_url)
        await r.ping()
        await r.aclose()
        return True
    except Exception:
        return False