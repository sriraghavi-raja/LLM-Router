import anthropic
from app.models.base import BaseLLM
from app.config import get_settings
 
 
class AnthropicModel(BaseLLM):
    def __init__(self):
        settings = get_settings()
        self._client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
        self._model = "claude-haiku-4-5"
 
    @property
    def name(self) -> str:
        return self._model
 
    @property
    def cost_per_1k_tokens(self) -> float:
        return 0.00025
 
    async def complete(self, prompt: str, max_tokens: int = 1000) -> str:
        message = await self._client.messages.create(
            model=self._model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text