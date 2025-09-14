import sys
import os
import time
import threading

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from cache import InMemoryCache
from models import CacheItem

def test_basic_operations():
    print("Basic Operations")
    cache = InMemoryCache(max_size=3)
    cache.put("key1", "value1")
    cache.put("key2", "value2")
    
    result1 = cache.get("key1")
    result2 = cache.get("key2")
    result3 = cache.get("nonexistent")
    
    print(f"Get key1: {result1}")
    print(f"Get key2: {result2}")
    print(f"Get nonexistent: {result3}")
    
    assert result1 == "value1", "Get operation failed for key1"
    assert result2 == "value2", "Get operation failed for key2"
    assert result3 is None, "Should return None for missing keys"
    
    print("Basic PUT / GET operations work")
    
    size = cache.size()
    print(f"Cache size: {size}")
    assert size == 2, f"Expected size 2, got {size}"
    print("Size tracking works")

def test_eviction_strategies():
    print("\nTesting Eviction Strategies")
    strategies = ['lru', 'mru', 'lfu', 'fifo']
    
    for strategy in strategies:
        print(f"Testing {strategy.upper()} strategy...")
        cache = InMemoryCache(max_size=2, eviction_strategy=strategy)
    
        cache.put("a", 1)
        cache.put("b", 2)
        cache.get("a")
        cache.put("c", 3)
        
        a_val = cache.get("a")
        b_val = cache.get("b")
        c_val = cache.get("c")
        
        print(f"  After eviction - a: {a_val}, b: {b_val}, c: {c_val}")
        assert c_val == 3, f"Newly added item should be present in {strategy}"
        
        print(f"{strategy.upper()} strategy working")

def test_ttl():
    print("\nTesting TTL")
    cache = InMemoryCache()
    cache.put("temp", "temporary_value", ttl=0.2)  # 200ms
    immediate_result = cache.get("temp")
    print(f"Immediate access: {immediate_result}")
    assert immediate_result == "temporary_value", "Should get value immediately"

    print("Waiting for TTL expiration...")
    time.sleep(0.3)
    expired_result = cache.get("temp")
    print(f"After expiration: {expired_result}")
    assert expired_result is None, "Should return None after TTL expiration"
    print("TTL expiration works")

def test_stats():
    print("\nTesting Stats")
    cache = InMemoryCache()
    
    cache.put("key", "value")
    cache.get("key")
    cache.get("missing")
    
    stats = cache.stats()
    print(f"Stats: {stats}")
    
    assert stats['hits'] >= 1, f"Expected at least 1 hit, got {stats['hits']}"
    assert stats['misses'] >= 1, f"Expected at least 1 miss, got {stats['misses']}"
    assert stats['current_size'] == 1, f"Expected size 1, got {stats['current_size']}"
    
    print("Stats tracking works")

def test_cache_overflow():
    print("\nTesting Cache Overflow")
    cache = InMemoryCache(max_size=3)
    for i in range(3):
        cache.put(f"key{i}", f"value{i}")
    
    print(f"Cache size after filling: {cache.size()}")
    assert cache.size() == 3, "Cache should be at max capacity"
    cache.put("overflow", "overflow_value")
    
    print(f"Cache size after overflow: {cache.size()}")
    assert cache.size() == 3, "Cache should still be at max capacity after eviction"
    overflow_result = cache.get("overflow")
    print(f"Overflow item: {overflow_result}")
    assert overflow_result == "overflow_value", "New item should be in cache"
    
    print("Cache overflow and eviction works")

def test_delete_and_clear():
    print("\nTesting Delete and Clear")
    cache = InMemoryCache()
    
    cache.put("delete_me", "value1")
    cache.put("keep_me", "value2")
    
    deleted = cache.delete("delete_me")
    assert deleted == True, "Delete should return True for existing key"
    assert cache.get("delete_me") is None, "Deleted item should not be retrievable"
    assert cache.get("keep_me") == "value2", "Other items should remain"
    
    print("Delete operation works")
    cache.clear()
    assert cache.size() == 0, "Cache should be empty after clear"
    assert cache.get("keep_me") is None, "No items should remain after clear"
    
    print("Clear operation works")

def run_all_tests():
    print("Cache Library Test Suite")
    tests = [
        test_basic_operations,
        test_eviction_strategies,
        test_ttl,
        test_stats,
        test_cache_overflow,
        test_delete_and_clear,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"{test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"{test.__name__} ERROR: {e}")
            failed += 1
        print() 
    print(f"Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("All tests passed!")
        return True
    else:
        print("Some tests failed!")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)