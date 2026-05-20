from abc import ABC, abstractmethod
 
 
class BaseLLM(ABC):
 
    @abstractmethod
    async def complete(self, prompt: str, max_tokens: int) -> str:
        """Send prompt to LLM and return the response string."""
        ...
 
    @property
    @abstractmethod
    def name(self) -> str:
        """Return a human-readable model name string."""
        ...
 
    @property
    @abstractmethod
    def cost_per_1k_tokens(self) -> float:
        """Return the cost in USD per 1000 tokens."""
        ...