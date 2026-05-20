from fastapi import APIRouter, Depends
import redis.asyncio as aioredis
 
from app.api.schemas import ChatRequest, ChatResponse, HealthResponse
from app.router.router import LLMRouter
from app.cache.redis_client import get_redis, health_check
from app.monitoring.metrics import (
    llm_requests_total, llm_latency_seconds, llm_cost_usd_total,
    cache_hits_total, cache_misses_total, cache_size_items,
)
 
api_router = APIRouter()
_llm_router = LLMRouter()
 
 
@api_router.post("/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest,
               redis: aioredis.Redis = Depends(get_redis)):
    result = await _llm_router.route(
        prompt=request.prompt,
        max_tokens=request.max_tokens,
        force_model=request.force_model,
        redis=redis,
    )
    labels = {"model": result.model_used, "cache_hit": str(result.cache_hit)}
    llm_requests_total.labels(**labels).inc()
    llm_latency_seconds.labels(model=result.model_used).observe(result.latency_ms/1000)
    llm_cost_usd_total.labels(model=result.model_used).inc(result.cost_estimate)
    if result.cache_hit: cache_hits_total.inc()
    else: cache_misses_total.inc()
    return ChatResponse(**result.__dict__)
 
 
@api_router.get("/health", response_model=HealthResponse)
async def health():
    redis_ok = await health_check()
    return HealthResponse(
        status="ok" if redis_ok else "degraded",
        redis_connected=redis_ok,
        models_available=["llama3", "claude-haiku-4-5", "gpt-4o-mini"],
    )
 
 
@api_router.get("/cache/stats")
async def cache_stats(redis: aioredis.Redis = Depends(get_redis)):
    keys = await redis.keys("sem_cache:*")
    total = len(keys)
    hits = cache_hits_total._value.get()
    misses = cache_misses_total._value.get()
    total_req = hits + misses
    hit_rate = hits / total_req if total_req > 0 else 0.0
    cache_size_items.set(total)
    return {"cached_items": total, "hit_rate": round(hit_rate, 4),
            "total_hits": int(hits), "total_misses": int(misses)}