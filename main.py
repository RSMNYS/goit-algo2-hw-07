import sys
import os

def print_header(title: str):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def print_separator():
    """Print separator line"""
    print("\n" + "-" * 80 + "\n")

def run_task_1():
    """Run Task 1: LRU Cache Optimization"""
    print_header("ЗАВДАННЯ 1: ОПТИМІЗАЦІЯ ДОСТУПУ ДО ДАНИХ З LRU-КЕШЕМ")
    
    try:
        # Import task 1 functions (assuming they're in the same file or importable)
        from task_lru_cache import run_performance_test
        
        print("Запуск тестування продуктивності LRU-кешу...")
        print("Порівняння швидкості обробки запитів з кешем та без кешу")
        print()
        
        # Run the performance test
        time_no_cache, time_with_cache, speedup = run_performance_test()
        
        print_separator()
        print("Завдання 1 виконано успішно!")
        print(f"   Прискорення: ×{speedup:.1f}")
        
    except ImportError as e:
        print(f"Помилка імпорту: {e}")
    except Exception as e:
        print(f"Помилка виконання: {e}")

def run_task_2():
    """Run Task 2: Fibonacci Performance Comparison"""
    print_header("ЗАВДАННЯ 2: ПОРІВНЯННЯ ФІБОНАЧЧІ З LRU CACHE ТА SPLAY TREE")
    
    try:
        # Import task 2 functions
        from task_fibonacci_comparison import main as fibonacci_main
        
        print("Запуск порівняльного аналізу алгоритмів обчислення чисел Фібоначчі...")
        print("Порівняння LRU Cache та Splay Tree")
        print()
        
        # Run the Fibonacci comparison
        fibonacci_main()
        
        print_separator()
        print("Завдання 2 виконано успішно!")
        print("   Графік збережено та результати виведено в таблиці")
        
    except ImportError as e:
        print(f"Помилка імпорту: {e}")
    except Exception as e:
        print(f"Помилка виконання: {e}")

def show_menu():
    """Show interactive menu"""
    print_header("ДЗ 7: АЛГОРИТМИ КЕРУВАННЯ КЕШЕМ")
    print()
    print("Оберіть завдання для виконання:")
    print("1. Завдання 1: Оптимізація доступу до даних з LRU-кешем")
    print("2. Завдання 2: Порівняння продуктивності Фібоначчі")
    print("0. Вихід")
    print()

def main():
    """Main function with interactive menu"""
    while True:
        try:
            show_menu()
            choice = input("Ваш вибір (0-2): ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                run_task_1()
            elif choice == "2":
                run_task_2()
            else:
                print("Невірний вибір. Спробуйте ще раз.")
            
            input("\nНатисніть Enter для продовження...")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Несподівана помилка: {e}")
            input("Натисніть Enter для продовження...")

if __name__ == "__main__":
    # Check if running with command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["1", "task1"]:
            run_task_1()
        elif arg in ["2", "task2"]:
            run_task_2()

        else:
            print("Використання:")
            print("  python main.py 1      # Запустити завдання 1")
            print("  python main.py 2      # Запустити завдання 2") 
            print("  python main.py        # Інтерактивне меню")
    else:
        main()