# In-Memory Cache Library
A performance, thread-safe in-memory caching library for Python with multiple eviction strategies, TTL support, and comprehensive statistics tracking.

## Features
- **Multiple Eviction Strategies**: LRU, MRU, LFU, FIFO
- **TTL Support**: Automatic expiration of cached items
- **Thread-Safe**: Built-in locking for concurrent access
- **Statistics Tracking**: Hit rate, miss rate, evictions, and more
- **Flexible Configuration**: Configurable cache size and eviction policies
- **Clean API**: Simple and intuitive interface

## Installation
Clone this repository and import the cache module:

```python
from cache import InMemoryCache
```

## Quick Start

```python
from cache import InMemoryCache

# Create a cache with default settings (LRU, max_size=100)
cache = InMemoryCache()

# Store items
cache.put("user:123", {"name": "Alice", "age": 30})
cache.put("session:abc", "active_session")

# Retrieve items
user = cache.get("user:123")
session = cache.get("session:abc")

# Items not found return None
missing = cache.get("nonexistent")  # Returns None
```

## Configuration Options

### Cache Size and Eviction Strategy

```python
# Create cache with custom size and eviction strategy
cache = InMemoryCache(
    max_size=1000,           # Maximum number of items
    eviction_strategy='lru'   # 'lru', 'mru', 'lfu', or 'fifo'
)
```

### TTL (Time To Live)

```python
# Store item with 5-second expiration
cache.put("temp_data", "expires_soon", ttl=5.0)

# Store item with 1-hour expiration
cache.put("session", "user_session", ttl=3600.0)
```

## Eviction Strategies

### LRU (Least Recently Used) - Default
Evicts the item that was accessed least recently.

```python
cache = InMemoryCache(max_size=2, eviction_strategy='lru')
cache.put("a", 1)
cache.put("b", 2)
cache.get("a")       # Access 'a' to make it recently used
cache.put("c", 3)    # This evicts 'b' (least recently used)
```

### MRU (Most Recently Used)
Evicts the item that was accessed most recently.

```python
cache = InMemoryCache(max_size=2, eviction_strategy='mru')
cache.put("a", 1)
cache.put("b", 2)
cache.get("a")       # Access 'a' to make it recently used
cache.put("c", 3)    # This evicts 'a' (most recently used)
```

### LFU (Least Frequently Used)
Evicts the item with the lowest access count.

```python
cache = InMemoryCache(max_size=2, eviction_strategy='lfu')
cache.put("a", 1)
cache.put("b", 2)
cache.get("a")       # Access 'a' twice
cache.get("a")
cache.put("c", 3)    # This evicts 'b' (accessed less frequently)
```

### FIFO (First In, First Out)
Evicts the oldest item regardless of access patterns.

```python
cache = InMemoryCache(max_size=2, eviction_strategy='fifo')
cache.put("a", 1)    # First in
cache.put("b", 2)
cache.put("c", 3)    # This evicts 'a' (first in, first out)
```

## API Reference

### Core Methods

#### `put(key: str, value: Any, ttl: Optional[float] = None)`
Store an item in the cache.

- **key**: String key for the item
- **value**: Any Python object to cache
- **ttl**: Optional time-to-live in seconds

```python
cache.put("user:123", {"name": "Alice"})
cache.put("temp", "data", ttl=300)  # Expires in 5 minutes
```

#### `get(key: str) -> Optional[Any]`
Retrieve an item from the cache.

- **Returns**: The cached value or `None` if not found/expired

```python
value = cache.get("user:123")
if value is not None:
    print(f"Found: {value}")
```

#### `delete(key: str) -> bool`
Remove an item from the cache.

- **Returns**: `True` if item was deleted, `False` if not found

```python
deleted = cache.delete("user:123")
```

#### `clear()`
Remove all items from the cache.

```python
cache.clear()
```

### Utility Methods

#### `size() -> int`
Get the current number of items in the cache.

```python
current_size = cache.size()
```

#### `keys() -> List[str]`
Get a list of all keys currently in the cache.

```python
all_keys = cache.keys()
```

#### `stats() -> Dict[str, Any]`
Get comprehensive cache statistics.

```python
stats = cache.stats()
print(f"Hit rate: {stats['hit_rate']}")
print(f"Total requests: {stats['total_requests']}")
```

Statistics include:
- `hits`: Number of successful retrievals
- `misses`: Number of failed retrievals
- `evictions`: Number of items evicted due to space constraints
- `expired`: Number of items that expired
- `total_requests`: Total get operations
- `hit_rate`: Percentage of successful retrievals
- `current_size`: Current number of items

#### `cleanup_expired() -> int`
Manually remove expired items and return the count.

```python
expired_count = cache.cleanup_expired()
print(f"Cleaned up {expired_count} expired items")
```

## Thread Safety

The cache is thread-safe and can be safely used in multi-threaded applications:

```python
import threading
from concurrent.futures import ThreadPoolExecutor

cache = InMemoryCache(max_size=1000)

def worker(thread_id):
    for i in range(100):
        cache.put(f"thread{thread_id}_item{i}", f"value_{i}")
        value = cache.get(f"thread{thread_id}_item{i}")

# Safe to use with multiple threads
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(worker, i) for i in range(4)]
    for future in futures:
        future.result()
```

## Error Handling

The library includes proper error handling for common issues:

```python
# Invalid cache size
try:
    cache = InMemoryCache(max_size=0)  # Raises ValueError
except ValueError as e:
    print(f"Error: {e}")

# Invalid eviction strategy
try:
    cache = InMemoryCache(eviction_strategy='invalid')  # Raises ValueError
except ValueError as e:
    print(f"Error: {e}")

# Invalid TTL
try:
    cache.put("key", "value", ttl=-1)  # Raises ValueError
except ValueError as e:
    print(f"Error: {e}")
```

## Performance Characteristics

- **Get Operations**: O(1) average case
- **Put Operations**: O(1) average case for most strategies
- **Memory Usage**: Linear with the number of cached items
- **Thread Contention**: Minimal due to efficient locking

### Benchmark Results

Single-threaded performance (typical results):
- **Writes**: ~500,000 operations/second
- **Reads**: ~1,000,000 operations/second

Multi-threaded performance scales well with concurrent access.

## Examples

### Web Session Cache

```python
# Cache user sessions with 1-hour expiration
session_cache = InMemoryCache(max_size=10000, eviction_strategy='lru')

def store_session(session_id, user_data):
    session_cache.put(f"session:{session_id}", user_data, ttl=3600)

def get_session(session_id):
    return session_cache.get(f"session:{session_id}")
```

### Database Query Cache

```python
# Cache database query results
query_cache = InMemoryCache(max_size=500, eviction_strategy='lfu')

def cached_query(sql, params):
    cache_key = f"{sql}:{hash(str(params))}"
    result = query_cache.get(cache_key)
    
    if result is None:
        result = execute_database_query(sql, params)
        query_cache.put(cache_key, result, ttl=300)  # 5-minute cache
    
    return result
```

### API Response Cache

```python
# Cache API responses with different TTL based on data type
api_cache = InMemoryCache(max_size=1000, eviction_strategy='lru')

def cache_api_response(endpoint, data, cache_duration=60):
    api_cache.put(f"api:{endpoint}", data, ttl=cache_duration)

# Cache static data for 1 hour
cache_api_response("/static/config", config_data, 3600)

# Cache dynamic data for 1 minute
cache_api_response("/live/prices", price_data, 60)
```

## Best Practices

1. **Choose the Right Eviction Strategy**:
   - Use **LRU** for general-purpose caching
   - Use **LFU** for data with predictable access patterns
   - Use **FIFO** for time-sensitive data
   - Use **MRU** for specialized cache replacement scenarios

2. **Set Appropriate TTL**:
   - Use TTL for time-sensitive data
   - Consider data freshness requirements
   - Balance between performance and data accuracy

3. **Monitor Cache Performance**:
   ```python
   # Regularly check cache statistics
   stats = cache.stats()
   if stats['hit_rate'] < 0.8:  # Less than 80% hit rate
       print("Consider increasing cache size or adjusting TTL")
   ```

4. **Handle None Returns**:
   ```python
   # Always check for None returns
   value = cache.get("key")
   if value is not None:
       # Use the cached value
       process_data(value)
   else:
       # Fetch from source and cache
       value = fetch_from_database()
       cache.put("key", value, ttl=300)
   ```

## Requirements
- Python 3.9+
- No external dependencies
## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.
