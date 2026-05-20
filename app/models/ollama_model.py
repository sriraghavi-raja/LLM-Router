import httpx

from app.models.base import BaseLLM
from app.config import get_settings


class OllamaModel(BaseLLM):

    def __init__(self):

        settings = get_settings()

        self._base_url = settings.ollama_base_url

        self._model = "phi3:mini"  # Changed from phi3

    @property
    def name(self) -> str:
        return self._model

    @property
    def cost_per_1k_tokens(self) -> float:
        return 0.0

    async def complete(
        self,
        prompt: str,
        max_tokens: int = 1000
    ) -> str:

        async with httpx.AsyncClient(timeout=60.0) as client:

            response = await client.post(
                f"{self._base_url}/api/generate",
                json={
                    "model": self._model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens,
                        "num_think": 0  # Disable thinking mode to save tokens
                    },
                },
            )

            response.raise_for_status()
            data = response.json()
            print(data)
            # Handle both standard response and extended thinking models
            result = data.get("response", "")
            if not result and "thinking" in data:
                result = data.get("thinking", "")
            return result