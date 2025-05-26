import random
import time
from typing import List, Tuple

class LRUCache:
    """Simple LRU Cache implementation"""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.order = []
    
    def get(self, key) -> int:
        if key in self.cache:
            # Move to end (most recently used)
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key]
        return -1
    
    def put(self, key, value) -> None:
        if key in self.cache:
            # Update existing key
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            # Remove least recently used
            oldest = self.order.pop(0)
            del self.cache[oldest]
        
        self.cache[key] = value
        self.order.append(key)
    
    def keys(self):
        """Return all keys in cache"""
        return list(self.cache.keys())
    
    def remove(self, key):
        """Remove key from cache"""
        if key in self.cache:
            del self.cache[key]
            self.order.remove(key)

# Initialize LRU cache with capacity 1000
cache = LRUCache(1000)

def range_sum_no_cache(array: List[int], left: int, right: int) -> int:
    """Calculate sum without caching"""
    return sum(array[left:right + 1])

def update_no_cache(array: List[int], index: int, value: int) -> None:
    """Update element without caching"""
    array[index] = value

def range_sum_with_cache(array: List[int], left: int, right: int) -> int:
    """Calculate sum with LRU caching"""
    key = (left, right)
    cached_result = cache.get(key)
    
    if cached_result != -1:
        return cached_result
    
    # Cache miss - compute sum
    result = sum(array[left:right + 1])
    cache.put(key, result)
    return result

def update_with_cache(array: List[int], index: int, value: int) -> None:
    """Update element and invalidate affected cache entries"""
    array[index] = value
    
    # Invalidate cache entries that contain the changed index
    keys_to_remove = []
    for key in cache.keys():
        left, right = key
        if left <= index <= right:
            keys_to_remove.append(key)
    
    for key in keys_to_remove:
        cache.remove(key)

def make_queries(n: int, q: int, hot_pool: int = 30, p_hot: float = 0.95, p_update: float = 0.03) -> List[Tuple]:
    """Generate queries for testing"""
    hot = [(random.randint(0, n//2), random.randint(n//2, n-1))
           for _ in range(hot_pool)]
    queries = []
    
    for _ in range(q):
        if random.random() < p_update:        # ~3% queries are Update
            idx = random.randint(0, n-1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:                                 # ~97% are Range
            if random.random() < p_hot:       # 95% are "hot" ranges
                left, right = random.choice(hot)
            else:                             # 5% are random ranges
                left = random.randint(0, n-1)
                right = random.randint(left, n-1)
            queries.append(("Range", left, right))
    
    return queries

def run_performance_test():
    """Run performance comparison test"""
    # Initialize parameters
    n = 100_000
    q = 50_000
    
    # Generate array
    array = [random.randint(1, 100) for _ in range(n)]
    
    # Generate queries
    queries = make_queries(n, q)
    
    print("Запуск тестування продуктивності...")
    print(f"Розмір масиву: {n:,}")
    print(f"Кількість запитів: {q:,}")
    print()
    
    # Test without cache
    array_copy1 = array.copy()
    start_time = time.time()
    
    for query in queries:
        if query[0] == "Range":
            _, left, right = query
            range_sum_no_cache(array_copy1, left, right)
        else:  # Update
            _, index, value = query
            update_no_cache(array_copy1, index, value)
    
    time_no_cache = time.time() - start_time
    
    # Test with cache
    array_copy2 = array.copy()
    cache.__init__(1000)  # Reset cache
    start_time = time.time()
    
    for query in queries:
        if query[0] == "Range":
            _, left, right = query
            range_sum_with_cache(array_copy2, left, right)
        else:  # Update
            _, index, value = query
            update_with_cache(array_copy2, index, value)
    
    time_with_cache = time.time() - start_time
    
    # Calculate speedup
    speedup = time_no_cache / time_with_cache if time_with_cache > 0 else float('inf')
    
    # Display results
    print("Результати тестування:")
    print(f"Без кешу :  {time_no_cache:.2f} c")
    print(f"LRU-кеш  :   {time_with_cache:.2f} c  (прискорення ×{speedup:.1f})")
    print()
    
    # Cache statistics
    print(f"Розмір кешу наприкінці: {len(cache.cache)} записів")
    
    return time_no_cache, time_with_cache, speedup

if __name__ == "__main__":
    # Set random seed for reproducible results
    random.seed(42)
    
    # Run the performance test
    run_performance_test()