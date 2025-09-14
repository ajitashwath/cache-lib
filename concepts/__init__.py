from .base import Eviction
from .lru import LRU
from .mru import MRU
from .lfu import LFU
from .fifo import FIFO

__all__ = ["Eviction", "LRU", "MRU", "LFU", "FIFO"]