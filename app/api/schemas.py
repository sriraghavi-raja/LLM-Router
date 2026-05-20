from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ChatRequest(BaseModel):
    prompt: str = Field(..., description="User prompt")
    max_tokens: int = Field(1000, description="Max response tokens")
    force_model: Optional[str] = Field(None, description="Override routing")


class ChatResponse(BaseModel):

    model_config = ConfigDict(
        protected_namespaces=()
    )

    response: str
    model_used: str
    cache_hit: bool
    latency_ms: float
    cost_estimate: float
 
class HealthResponse(BaseModel):
    status: str
    redis_connected: bool
    models_available: list[str]