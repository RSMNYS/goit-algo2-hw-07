import timeit
import matplotlib.pyplot as plt
from functools import lru_cache
from typing import Optional

class SplayNode:
    """Node for Splay Tree"""
    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.left: Optional['SplayNode'] = None
        self.right: Optional['SplayNode'] = None

class SplayTree:
    """Splay Tree implementation for caching Fibonacci values"""
    def __init__(self):
        self.root: Optional[SplayNode] = None
    
    def _right_rotate(self, x: SplayNode) -> SplayNode:
        """Perform right rotation"""
        y = x.left
        x.left = y.right
        y.right = x
        return y
    
    def _left_rotate(self, x: SplayNode) -> SplayNode:
        """Perform left rotation"""
        y = x.right
        x.right = y.left
        y.left = x
        return y
    
    def _splay(self, root: Optional[SplayNode], key: int) -> Optional[SplayNode]:
        """Splay operation to move key to root"""
        if not root or root.key == key:
            return root
        
        # Key is in left subtree
        if key < root.key:
            if not root.left:
                return root
            
            # Zig-Zig (Left Left)
            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._right_rotate(root)
            
            # Zig-Zag (Left Right)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right:
                    root.left = self._left_rotate(root.left)
            
            # Do first rotation for root
            return self._right_rotate(root) if root.left else root
        
        # Key is in right subtree
        else:
            if not root.right:
                return root
            
            # Zig-Zag (Right Left)
            if key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left:
                    root.right = self._right_rotate(root.right)
            
            # Zig-Zig (Right Right)
            elif key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._left_rotate(root)
            
            # Do first rotation for root
            return self._left_rotate(root) if root.right else root
    
    def search(self, key: int) -> Optional[int]:
        """Search for key and return value if found"""
        self.root = self._splay(self.root, key)
        if self.root and self.root.key == key:
            return self.root.value
        return None
    
    def insert(self, key: int, value: int) -> None:
        """Insert key-value pair"""
        if not self.root:
            self.root = SplayNode(key, value)
            return
        
        self.root = self._splay(self.root, key)
        
        if self.root.key == key:
            self.root.value = value
            return
        
        new_node = SplayNode(key, value)
        
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
        
        self.root = new_node

@lru_cache(maxsize=None)
def fibonacci_lru(n: int) -> int:
    """Calculate Fibonacci number using LRU cache"""
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

def fibonacci_splay(n: int, tree: SplayTree) -> int:
    """Calculate Fibonacci number using Splay Tree"""
    if n <= 1:
        return n
    
    # Check if already computed
    cached_result = tree.search(n)
    if cached_result is not None:
        return cached_result
    
    # Compute recursively
    result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, result)
    return result

def measure_fibonacci_performance():
    """Measure and compare Fibonacci computation performance"""
    # Test values: 0 to 950 with step 50
    test_values = list(range(0, 951, 50))
    lru_times = []
    splay_times = []
    
    print("Вимірювання продуктивності обчислення чисел Фібоначчі...")
    print("Це може зайняти деякий час для великих значень n...")
    print()
    
    for n in test_values:
        print(f"Тестування n = {n}...")
        
        # Measure LRU cache performance
        fibonacci_lru.cache_clear()  # Clear cache before each test
        lru_time = timeit.timeit(
            lambda: fibonacci_lru(n),
            number=1
        )
        lru_times.append(lru_time)
        
        # Measure Splay Tree performance
        splay_tree = SplayTree()  # Fresh tree for each test
        splay_time = timeit.timeit(
            lambda: fibonacci_splay(n, splay_tree),
            number=1
        )
        splay_times.append(splay_time)
    
    return test_values, lru_times, splay_times

def print_results_table(test_values, lru_times, splay_times):
    """Print formatted results table"""
    print("\nРезультати вимірювання часу виконання:")
    print("-" * 60)
    print(f"{'n':<10} {'LRU Cache Time (s)':<20} {'Splay Tree Time (s)':<20}")
    print("-" * 60)
    
    for n, lru_time, splay_time in zip(test_values, lru_times, splay_times):
        print(f"{n:<10} {lru_time:.8f}           {splay_time:.8f}")
    
    print("-" * 60)

def create_performance_graph(test_values, lru_times, splay_times):
    """Create performance comparison graph"""
    plt.figure(figsize=(12, 8))
    
    plt.plot(test_values, lru_times, 'b-o', label='LRU Cache', linewidth=2, markersize=6)
    plt.plot(test_values, splay_times, 'r-s', label='Splay Tree', linewidth=2, markersize=6)
    
    plt.xlabel('Число Фібоначчі (n)', fontsize=12)
    plt.ylabel('Середній час виконання (секунди)', fontsize=12)
    plt.title('Порівняння часу виконання для LRU Cache та Splay Tree', fontsize=14)
    
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Use scientific notation for y-axis if needed
    plt.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
    
    plt.tight_layout()
    plt.show()

def analyze_results(test_values, lru_times, splay_times):
    """Analyze and print conclusions about the results"""
    print("\nАналіз результатів:")
    print("=" * 50)
    
    # Calculate average times
    avg_lru = sum(lru_times) / len(lru_times)
    avg_splay = sum(splay_times) / len(splay_times)
    
    print(f"Середній час LRU Cache: {avg_lru:.8f} секунд")
    print(f"Середній час Splay Tree: {avg_splay:.8f} секунд")
    
    if avg_lru < avg_splay:
        speedup = avg_splay / avg_lru
        print(f"LRU Cache швидший в {speedup:.2f} разів в середньому")
    else:
        speedup = avg_lru / avg_splay
        print(f"Splay Tree швидший в {speedup:.2f} разів в середньому")
    
    # Find best and worst cases
    lru_best = min(lru_times)
    lru_worst = max(lru_times)
    splay_best = min(splay_times)
    splay_worst = max(splay_times)
    
    print(f"\nНайкращий час LRU Cache: {lru_best:.8f} с")
    print(f"Найгірший час LRU Cache: {lru_worst:.8f} с")
    print(f"Найкращий час Splay Tree: {splay_best:.8f} с")
    print(f"Найгірший час Splay Tree: {splay_worst:.8f} с")
    
    # Performance trend analysis
    print("\nВисновки:")
    print("- LRU Cache використовує вбудовану оптимізацію Python")
    print("- Splay Tree має додаткові витрати на ротації та пошук")
    print("- Для великих значень n LRU Cache показує кращу продуктивність")
    print("- Різниця в продуктивності збільшується зі зростанням n")

def main():
    """Main function to run the Fibonacci performance comparison"""
    print("Завдання 2: Порівняння продуктивності обчислення чисел Фібоначчі")
    print("Порівняння LRU Cache та Splay Tree")
    print("=" * 60)
    
    # Measure performance
    test_values, lru_times, splay_times = measure_fibonacci_performance()
    
    # Print results table
    print_results_table(test_values, lru_times, splay_times)
    
    # Analyze results
    analyze_results(test_values, lru_times, splay_times)
    
    # Create graph
    print("\nСтворення графіка...")
    create_performance_graph(test_values, lru_times, splay_times)
    
    print("\nВиконання завершено!")

if __name__ == "__main__":
    main()