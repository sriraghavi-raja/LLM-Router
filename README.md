
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

###ScreenShots of the Working

<img width="1536" height="662" alt="image" src="https://github.com/user-attachments/assets/dd63d3d8-a05c-4099-be87-e786ee80a8c2" />

<img width="1533" height="739" alt="Screenshot 2026-05-20 130350" src="https://github.com/user-attachments/assets/32fb244a-9584-46b9-b4c8-2d792ad178a0" />


<img width="1536" height="744" alt="image" src="https://github.com/user-attachments/assets/542e9581-68ee-4fd9-af29-33925e8a1503" />

<img width="1536" height="742" alt="Screenshot 2026-05-20 130518" src="https://github.com/user-attachments/assets/5bc59fbd-c1a1-475a-8b47-51aa5ab6471c" />



## How It Works

The LLM Router intelligently processes queries while minimizing costs through semantic caching.

### Request Flow (Step-by-Step)

1. **User Submits Query**
   - Type your question in the dashboard's Query Composer
   - System receives the query through the `/v1/chat` API

2. **Embedding Generation**
   - Query converted to a 384-dimensional vector embedding
   - Uses SentenceTransformers (all-MiniLM-L6-v2 model)
   - Embedding captures semantic meaning of the question

3. **Semantic Cache Lookup**
   - System searches Redis cache for similar previous queries
   - Compares embeddings using cosine similarity
   - **Similarity Threshold: 0.70** (paraphrased questions matching ≥70% treated as cache hits)
   - ⚡ **If Cache Hit**: Returns cached response in ~10-50ms (90% latency savings)

4. **Complexity Classification** (if cache miss)
   - Analyzes query to determine complexity level (0.0-1.0 score)
   - **Low complexity (0-0.33)**: Simple factual questions
   - **Mid complexity (0.34-0.66)**: Requires reasoning
   - **High complexity (0.67-1.0)**: Complex analysis/coding

5. **Model Selection**
   - **Low complexity** → Ollama phi3:mini (free, local, fast)
   - **Mid complexity** → Anthropic Claude Haiku (if API key provided)
   - **High complexity** → OpenAI GPT-4o-mini (if API key provided)

6. **LLM Processing**
   - Selected model generates response with max 200 tokens
   - Ollama runs locally (~500-2000ms latency)
   - API-based models slightly slower but more capable

7. **Response Caching**
   - Response + embedding stored in Redis
   - 1-hour TTL (automatic expiration)
   - Future similar queries instantly retrieved from cache

8. **Return Results with Metadata**
   - Response text delivered to user
   - Dashboard shows:
     - ✓ Which model was used
     - ✓ Whether response came from cache
     - ✓ Processing latency
     - ✓ Complexity score
     - ✓ Cost estimate

### Dashboard Visualization

The interactive dashboard displays:

- **📊 Metrics Cards**: Track total requests, cache efficiency, hit rate, average latency
- **🏗️ Architecture Diagram**: Visual representation of the entire system flow
- **📝 Query Composer**: Built-in interface with preset examples (Similar/Different queries)
- **🎯 Cache Hit/Miss Chart**: Doughnut chart showing cache efficiency percentage
- **🤖 Model Usage Chart**: Bar chart showing which LLM models are being used most
- **⏱️ Latency Timeline**: Line chart tracking response times over requests
- **📋 Request History**: Detailed log of all queries with cache status and latency

### Key Benefits

| Feature | Benefit |
|---------|---------|
| **Semantic Caching** | 90% faster responses for similar questions |
| **Smart Routing** | Uses cheapest/fastest model for each query type |
| **Local Processing** | Ollama runs locally - no external API calls for simple queries |
| **Cost Efficient** | Dramatically reduces API costs through cache reuse |
| **Real-time Monitoring** | Dashboard shows exactly what's happening |

### Example Workflow
































