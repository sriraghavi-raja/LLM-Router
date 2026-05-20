import openai
from app.models.base import BaseLLM
from app.config import get_settings
 
 
class OpenAIModel(BaseLLM):
    def __init__(self):
        settings = get_settings()
        self._client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
        self._model = "gpt-4o-mini"
 
    @property
    def name(self) -> str:
        return self._model
 
    @property
    def cost_per_1k_tokens(self) -> float:
        return 0.00015
 
    async def complete(self, prompt: str, max_tokens: int = 1000) -> str:
        response = await self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content