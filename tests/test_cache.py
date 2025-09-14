import time
import unittest
from cache import InMemoryCache

class TestCache(unittest.TestCase):
    def setUp(self):
        self.cache = InMemoryCache(max_size=3)
    
    def test_basic_operations(self):
        self.cache.put("key1", "value1")
        self.assertEqual(self.cache.get("key1"), "value1")
        self.assertIsNone(self.cache.get("nonexistent"))
    
    def test_eviction(self):
        self.cache.put("a", 1)
        self.cache.put("b", 2)
        self.cache.put("c", 3)
        self.cache.put("d", 4)
        self.assertIsNone(self.cache.get("a"))
        self.assertEqual(self.cache.get("d"), 4)
    
    def test_ttl(self):
        self.cache.put("temp", "value", ttl=0.1)
        self.assertEqual(self.cache.get("temp"), "value")
        time.sleep(0.15)
        self.assertIsNone(self.cache.get("temp"))
    
    def test_delete(self):
        self.cache.put("key", "value")
        self.assertTrue(self.cache.delete("key"))
        self.assertFalse(self.cache.delete("key"))
        self.assertIsNone(self.cache.get("key"))
    
    def test_stats(self):
        self.cache.put("key", "value")
        self.cache.get("key")
        self.cache.get("nonexistent")
        stats = self.cache.stats()
        self.assertEqual(stats['hits'], 1)
        self.assertEqual(stats['misses'], 1)

if __name__ == "__main__":
    unittest.main()