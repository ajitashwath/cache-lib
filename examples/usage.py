import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cache import InMemoryCache

def basic_operations():
    print("Basic Operations")
    cache = InMemoryCache(max_size=3, eviction_strategy='lru')
    cache.put("user:1", {"name": "A", "age": 30})
    cache.put("user:2", {"name": "S", "age": 25})
    print("User 1:", cache.get("user:1"))
    print("User 2:", cache.get("user:2"))
    print("Stats:", cache.stats())
    print()

def ttl_example():
    print("TTL Example")
    cache = InMemoryCache()
    cache.put("session:abc", "active", ttl=2.0)
    print("Session (immediate):", cache.get("session:abc"))
    time.sleep(2.1)
    print("Session (expired):", cache.get("session:abc"))
    print()

def comparison():
    print("Strategy Comparison")
    strategies = ['lru', 'mru', 'lfu', 'fifo']
    for strategy in strategies:
        cache = InMemoryCache(max_size=2, eviction_strategy=strategy)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.get("a")
        cache.put("c", 3)
        print(f"{strategy.upper()}: a={cache.get('a')}, b={cache.get('b')}, c={cache.get('c')}")
    print()

def comprehensive_test():
    print("Comprehensive Test")
    cache = InMemoryCache(max_size=5, eviction_strategy='lru')
    for i in range(5):
        cache.put(f"key{i}", f"value{i}")
    
    print("Initial cache size:", cache.size())
    
    cache.get("key0")
    cache.get("key2")
    
    cache.put("key5", "value5")
    print("After eviction:")
    for i in range(6):
        result = cache.get(f"key{i}")
        print(f"key{i}: {result}")
    
    print("Final stats:", cache.stats())

if __name__ == "__main__":
    basic_operations()
    ttl_example()
    comparison()
    comprehensive_test()