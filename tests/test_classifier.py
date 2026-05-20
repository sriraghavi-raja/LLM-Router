import pytest
from app.classifier.complexity import classify
 
 
class TestLowTier:   # score 0.00-0.33 -> Ollama
    def test_simple_factual(self):
        score = classify("What is the capital of France?")
        assert score <= 0.33, f"Expected low, got {score}"
 
    def test_very_short_query(self):
        assert classify("Hi") <= 0.33
 
    def test_definition_question(self):
        assert classify("Define photosynthesis") <= 0.33
 
 
class TestMidTier:   # score 0.34-0.66 -> Haiku/GPT-4o-mini
    def test_reasoning_question(self):
        score = classify(
            "Why is Python popular for data science? Explain the trade-offs."
        )
        assert 0.34 <= score <= 0.66, f"Expected mid, got {score}"
 
    def test_comparison_question(self):
        score = classify(
            "Compare REST vs GraphQL and discuss pros and cons"
        )
        assert 0.34 <= score <= 0.66, f"Expected mid, got {score}"
 
 
class TestHighTier:  # score 0.67-1.00 -> Sonnet/GPT-4
    def test_complex_code_question(self):
        score = classify(
            "Implement a thread-safe LRU cache in Python using a doubly linked list "
            "and hash map. Include error handling, type hints, and unit tests."
        )
        assert score >= 0.67, f"Expected high, got {score}"
 
    def test_architecture_question(self):
        score = classify(
            "Design a microservices architecture for high-traffic e-commerce. "
            "Discuss database sharding, API gateway patterns, async event processing."
        )
        assert score >= 0.67, f"Expected high, got {score}"