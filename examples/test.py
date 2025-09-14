import sys
import os
import time
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cache import InMemoryCache

def benchmark_single_thread():
    cache = InMemoryCache(max_size=1000)
    start = time.time()
    for i in range(10000):
        cache.put(f"key_{i}", f"value_{i}")
    write_time = time.time() - start
    
    start = time.time()
    for i in range(10000):
        cache.get(f"key_{i}")
    read_time = time.time() - start
    print(f"Single-thread: {10000/write_time:.0f} writes/sec, {10000/read_time:.0f} reads/sec")

def benchmark_multi_thread():
    cache = InMemoryCache(max_size=1000)
    def worker(start_idx, count):
        for i in range(start_idx, start_idx + count):
            cache.put(f"key_{i}", f"value_{i}")
            cache.get(f"key_{i}")
    
    start = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(worker, i*2500, 2500) for i in range(4)]
        for future in futures:
            future.result()
    
    total_time = time.time() - start
    print(f"Multi-thread: {20000/total_time:.0f} ops/sec across 4 threads")

if __name__ == "__main__":
    benchmark_single_thread()
    benchmark_multi_thread()