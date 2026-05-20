from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator
from app.api.routes import api_router
from app.cache.redis_client import health_check
import os
 
 
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ──────────────────────────────
    redis_ok = await health_check()
    print(f"Redis connected: {redis_ok}")
 
    from app.cache.semantic_cache import SemanticCache
    app.state.cache = SemanticCache()   # pre-loads embedding model
    print("Embedding model loaded.")
 
    yield
 
    # ── Shutdown ─────────────────────────────
    from app.cache import redis_client
    if redis_client._redis_pool:
        await redis_client._redis_pool.aclose()
 
 
app = FastAPI(
    title="LLM Router API",
    description="Intelligent routing with semantic caching",
    version="1.0.0",
    lifespan=lifespan,
)

# Enable CORS for dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)
app.include_router(api_router)

# Root endpoint with links
@app.get("/")
async def root():
    return {
        "message": "🚀 LLM Router with Semantic Caching",
        "dashboard": "http://localhost:8000/static/dashboard.html",
        "api_docs": "http://localhost:8000/docs",
        "health": "http://localhost:8000/health",
        "cache_stats": "http://localhost:8000/cache/stats",
        "metrics": "http://localhost:8000/metrics",
    }

# Serve static files (dashboard)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
