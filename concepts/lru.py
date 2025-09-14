'''Least Recently Used'''

from collections import OrderedDict
from typing import Dict
from .base import Eviction
from models import CacheItem

class LRU(Eviction):
    def __init__(self):
        self.access_order = OrderedDict()
    
    def should_evict(self, key: str, item: CacheItem, cache_data: Dict[str, CacheItem]) -> str:
        return next(iter(self.access_order))
    
    def on_access(self, key: str, item: CacheItem):
        self.access_order.pop(key, None)
        self.access_order[key] = True