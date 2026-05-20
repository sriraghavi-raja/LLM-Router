import re
 
CODE_KEYWORDS = {
    "function", "class", "def ", "import", "return", "algorithm",
    "implement", "code", "debug", "error", "exception", "api",
    "async", "await", "database", "sql", "query", "loop", "recursion",
    "optimize", "refactor", "architecture", "design pattern",
}
 
REASONING_WORDS = {
    "why", "explain", "compare", "analyse", "analyze", "evaluate",
    "discuss", "pros and cons", "trade-off", "difference between",
    "how does", "what is the best", "recommend", "strategy",
}
 
FACTUAL_WORDS = {
    "what is", "who is", "when did", "where is", "define",
    "list", "name", "how many", "capital of",
}
 
 
def _token_score(prompt: str) -> float:
    word_count = len(prompt.split())
    return min(word_count / 300, 1.0)
 
 
def _code_score(prompt: str) -> float:
    lower = prompt.lower()
    return 1.0 if any(kw in lower for kw in CODE_KEYWORDS) else 0.0
 
 
def _reasoning_score(prompt: str) -> float:
    lower = prompt.lower()
    return 0.8 if any(kw in lower for kw in REASONING_WORDS) else 0.0
 
 
def _factual_score(prompt: str) -> float:
    lower = prompt.lower()
    return -0.3 if any(kw in lower for kw in FACTUAL_WORDS) else 0.0
 
 
def classify(prompt: str) -> float:
    """
    Score prompt complexity 0.0 - 1.0.
    0.00-0.33 -> Ollama | 0.34-0.66 -> Mid | 0.67-1.00 -> High
    """
    raw = (
        _token_score(prompt) * 0.3
        + _code_score(prompt) * 0.4
        + _reasoning_score(prompt) * 0.3
        + _factual_score(prompt)
    )
    return max(0.0, min(1.0, raw))