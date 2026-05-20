from prometheus_client import Counter, Histogram, Gauge
 
llm_requests_total = Counter(
    "llm_requests_total",
    "Total LLM requests processed",
    ["model", "cache_hit"],
)
 
llm_latency_seconds = Histogram(
    "llm_latency_seconds",
    "LLM response latency in seconds",
    ["model"],
    buckets=[0.1, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0],
)
 
llm_cost_usd_total = Counter(
    "llm_cost_usd_total",
    "Cumulative estimated cost in USD",
    ["model"],
)
 
cache_size_items = Gauge(
    "cache_size_items",
    "Number of items in the semantic cache",
)
 
cache_hits_total = Counter("cache_hits_total", "Total semantic cache hits")
cache_misses_total = Counter("cache_misses_total", "Total semantic cache misses")
