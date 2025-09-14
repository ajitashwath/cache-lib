'''First In First Out'''

from collections import OrderedDict
from typing import Dict
from .base import Eviction
from models import CacheItem


class FIFO(Eviction):
    def __init__(self):
        self.insertion_order = OrderedDict()
    
    def should_evict(self, key: str, item: CacheItem, cache_data: Dict[str, CacheItem]) -> str:
        return next(iter(self.insertion_order))
    
    def on_access(self, key: str, item: CacheItem):
        pass
    
    def on_insert(self, key: str):
        self.insertion_order[key] = True