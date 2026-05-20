import time
from dataclasses import dataclass
from typing import Optional

import redis.asyncio as aioredis

from app.cache.semantic_cache import SemanticCache
from app.models.ollama_model import OllamaModel


@dataclass
class RouterResponse:
    response: str
    model_used: str
    cache_hit: bool
    latency_ms: float
    cost_estimate: float


class LLMRouter:

    def __init__(self):
        self._cache = SemanticCache()
        self._model = OllamaModel()

    def _estimate_cost(self, response: str) -> float:
        return 0.0

    async def route(
        self,
        prompt: str,
        max_tokens: int = 1000,
        force_model: Optional[str] = None,
        redis: Optional[aioredis.Redis] = None
    ) -> RouterResponse:

        start = time.monotonic()

        # 1. Check semantic cache
        if redis:
            cached = await self._cache.get(prompt, redis)

            if cached:
                return RouterResponse(
                    response=cached,
                    model_used="cache",
                    cache_hit=True,
                    latency_ms=(time.monotonic() - start) * 1000,
                    cost_estimate=0.0
                )

        # 2. Generate response from Ollama
        response_text = await self._model.complete(
            prompt,
            max_tokens
        )

        # 3. Store in cache
        if redis:
            await self._cache.set(
                prompt,
                response_text,
                redis
            )

        # 4. Return response
        return RouterResponse(
            response=response_text,
            model_used=self._model.name,
            cache_hit=False,
            latency_ms=(time.monotonic() - start) * 1000,
            cost_estimate=0.0
        )