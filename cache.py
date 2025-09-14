import threading
import time
from typing import Any, Optional, Dict
from .models import CacheItem
from .concepts import LRU, MRU, LFU, FIFO

class InMemoryCache:
    STRATEGIES = {
        'lru': LRU,
        'mru': MRU,
        'lfu': LFU,
        'fifo': FIFO
    }
    
    def __init__(self, max_size: int = 100, eviction_strategy: str = 'lru'):
        if eviction_strategy not in self.STRATEGIES:
            raise ValueError(f"Unknown eviction strategy: {eviction_strategy}")
        
        self._max_size = max_size
        self._data: Dict[str, CacheItem] = {}
        self._lock = threading.RLock()
        self._strategy = self.STRATEGIES[eviction_strategy]()
        self._stats = {'hits': 0, 'misses': 0, 'evictions': 0, 'expired': 0}
    
    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key not in self._data:
                self._stats['misses'] += 1
                return None
            
            item = self._data[key]
            
            if item.is_expired():
                del self._data[key]
                self._cleanup_strategy_on_delete(key)
                self._stats['expired'] += 1
                self._stats['misses'] += 1
                return None
            
            item.touch()
            self._strategy.on_access(key, item)
            self._stats['hits'] += 1
            return item.value
    
    def put(self, key: str, value: Any, ttl: Optional[float] = None):
        with self._lock:
            item = CacheItem(value=value, created_at=time.time(), ttl=ttl, last_accessed=time.time())
            
            if key in self._data:
                self._data[key] = item
                self._strategy.on_access(key, item)
                return
            
            if len(self._data) >= self._max_size:
                self._evict_one()
            
            self._data[key] = item
            self._strategy.on_access(key, item)
            
            if hasattr(self._strategy, 'on_insert'):
                self._strategy.on_insert(key)
    
    def delete(self, key: str) -> bool:
        with self._lock:
            if key in self._data:
                del self._data[key]
                self._cleanup_strategy_on_delete(key)
                return True
            return False
    
    def clear(self):
        with self._lock:
            self._data.clear()
            if hasattr(self._strategy, 'access_order'):
                self._strategy.access_order.clear()
            if hasattr(self._strategy, 'insertion_order'):
                self._strategy.insertion_order.clear()
    
    def size(self) -> int:
        with self._lock:
            return len(self._data)
    
    def stats(self) -> Dict[str, Any]:
        with self._lock:
            total = self._stats['hits'] + self._stats['misses']
            hit_rate = self._stats['hits'] / total if total > 0 else 0
            return {**self._stats, 'total_requests': total, 'hit_rate': round(hit_rate, 3), 'current_size': len(self._data)}
    
    def cleanup_expired(self) -> int:
        with self._lock:
            expired_keys = [k for k, v in self._data.items() if v.is_expired()]
            for key in expired_keys:
                del self._data[key]
                self._cleanup_strategy_on_delete(key)
                self._stats['expired'] += 1
            return len(expired_keys)
    
    def _evict_one(self):
        if not self._data:
            return
        key_to_evict = self._strategy.should_evict(None, None, self._data)
        if key_to_evict in self._data:
            del self._data[key_to_evict]
            self._cleanup_strategy_on_delete(key_to_evict)
            self._stats['evictions'] += 1
    
    def _cleanup_strategy_on_delete(self, key: str):
        if hasattr(self._strategy, 'access_order'):
            self._strategy.access_order.pop(key, None)
        if hasattr(self._strategy, 'insertion_order'):
            self._strategy.insertion_order.pop(key, None)