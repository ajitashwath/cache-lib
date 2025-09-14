'''Least Frequently Used'''

from typing import Dict
from .base import Eviction
from ..models import CacheItem


class LFU(Eviction):
    def should_evict(self, key: str, item: CacheItem, cache_data: Dict[str, CacheItem]) -> str:
        return min(cache_data.keys(), key=lambda k: cache_data[k].access_count)
    
    def on_access(self, key: str, item: CacheItem):
        pass