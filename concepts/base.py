from abc import ABC, abstractmethod
from typing import Dict
from models import CacheItem


class Eviction(ABC):
    @abstractmethod
    def should_evict(self, key: str, item: CacheItem, cache_data: Dict[str, CacheItem]) -> str:
        pass
    
    @abstractmethod
    def on_access(self, key: str, item: CacheItem):
        pass