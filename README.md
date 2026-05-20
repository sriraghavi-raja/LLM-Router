@"
# LLM Router - Semantic Caching

Intelligent LLM routing with semantic cache intelligence, demonstrating efficient model selection and response caching.

## Features

- **Semantic Caching**: Redis-backed semantic similarity matching (threshold: 0.70)
- **Intelligent Routing**: 3-tier complexity-based model selection
- **FastAPI Server**: Modern async web framework with CORS support
- **Interactive Dashboard**: Real-time visualization of cache hits/misses and LLM performance
- **Prometheus Metrics**: Request tracking and analytics

## Architecture

- **Query Processing**: Client → FastAPI → SentenceTransformers (all-MiniLM-L6-v2)
- **Cache Layer**: Redis semantic embedding storage with 3600s TTL
- **Complexity Classification**: Determines model tier (Low/Mid/High)
- **Model Selection**:
  - Low (0.0-0.33): Ollama phi3:mini (local, free)
  - Mid (0.34-0.66): Anthropic Claude Haiku (optional)
  - High (0.67-1.0): OpenAI GPT-4o-mini (optional)

## Quick Start

### Prerequisites
- Python 3.11+
- Redis running at localhost:6379
- Ollama running at localhost:11434

### Installation

```bash
pip install -r requirements.txt
