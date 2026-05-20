import time
import numpy as np
import redis.asyncio as aioredis
from typing import Optional
from sentence_transformers import SentenceTransformer
from app.config import get_settings
 
CACHE_TTL = 3600        # 1 hour
KEY_PREFIX = "sem_cache:"
 
 
class SemanticCache:
    def __init__(self):
        settings = get_settings()
        self._threshold = settings.cache_similarity_threshold
        self._model = SentenceTransformer(settings.embedding_model)
 
    def embed(self, text: str) -> np.ndarray:
        """Convert query to 384-dim float32 vector."""
        return self._model.encode(text, convert_to_numpy=True)
 
    @staticmethod
    def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10))
 
    async def get(self, query: str, redis: aioredis.Redis) -> Optional[str]:
        new_vec = self.embed(query)
        cursor = 0
        best_score = 0.0
        best_response: Optional[str] = None
 
        while True:
            cursor, keys = await redis.scan(
                cursor, match=f"{KEY_PREFIX}*", count=100
            )
            for key in keys:
                data = await redis.hgetall(key)
                if not data:
                    continue
                stored_vec = np.frombuffer(data[b"embedding"], dtype=np.float32)
                score = self._cosine_similarity(new_vec, stored_vec)
                if score > best_score:
                    best_score = score
                    best_response = data[b"response"].decode("utf-8")
            if cursor == 0:
                break
 
        if best_score >= self._threshold:
            return best_response
        return None
 
    async def set(self, query: str, response: str, redis: aioredis.Redis) -> None:
        vec = self.embed(query)
        key = f"{KEY_PREFIX}{int(time.time() * 1000)}"
        await redis.hset(key, mapping={
            "embedding": vec.astype(np.float32).tobytes(),
            "response": response,
            "query": query,
        })
        await redis.expire(key, CACHE_TTL)