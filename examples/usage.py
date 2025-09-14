import time
from cache import InMemoryCache

def basic_operations():
    cache = InMemoryCache(max_size=3, eviction_strategy='lru')
    cache.put("user:1", {"name": "A", "age": 30})
    cache.put("user:2", {"name": "S", "age": 25})
    print("User 1:", cache.get("user:1"))
    print("User 2:", cache.get("user:2"))
    print("Stats:", cache.stats())

def ttl_example():
    cache = InMemoryCache()
    cache.put("session:abc", "active", ttl=2.0)
    print("Session (immediate):", cache.get("session:abc"))
    time.sleep(2.1)
    print("Session (expired):", cache.get("session:abc"))

def comparison():
    strategies = ['lru', 'mru', 'lfu', 'fifo']
    for strategy in strategies:
        cache = InMemoryCache(max_size=2, eviction_strategy=strategy)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.get("a")
        cache.put("c", 3)  
        print(f"{strategy.upper()}: a={cache.get('a')}, b={cache.get('b')}, c={cache.get('c')}")

if __name__ == "__main__":
    basic_operations()
    ttl_example()
    comparison()