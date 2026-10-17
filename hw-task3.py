import timeit
import random
import sys

# Збільшуємо ліміт рекурсії для сортування злиттям на великих списках
sys.setrecursionlimit(200000)

# --- 1. Реалізація сортування злиттям (Merge Sort) ---
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    return merge(left_half, right_half)

def merge(left, right):
    sorted_arr = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            sorted_arr.append(left[i])
            i += 1
        else:
            sorted_arr.append(right[j])
            j += 1
    sorted_arr.extend(left[i:])
    sorted_arr.extend(right[j:])
    return sorted_arr

# --- 2. Реалізація сортування вставками (Insertion Sort) ---
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

# --- 3. Функція тестування ---
def run_benchmarks():
    # Розміри тестових масивів
    sizes = [100, 1000, 5000, 10000]
    
    print(f"{'Розмір масиву':<15} | {'Алгоритм':<20} | {'Час виконання (секунди)':<25}")
    print("-" * 65)

    for size in sizes:
        # Генеруємо випадковий масив
        data = [random.randint(0, 100000) for _ in range(size)]
        
        # Для insertion sort на великих масивах обмежуємо розмір, щоб уникнути зависання (O(n^2) дуже повільне)
        if size > 10000:
            continue

        # Тест сортування вставками (тільки для невеликих і середніх розмірів через O(n^2))
        if size <= 5000:
            t_insertion = timeit.timeit(lambda: insertion_sort(data.copy()), number=3)
            print(f"{size:<15} | {'Insertion Sort':<20} | {t_insertion:<25.6f}")
        else:
            print(f"{size:<15} | {'Insertion Sort':<20} | {'Занадто довго (O(n^2))':<25}")

        # Тест сортування злиттям
        t_merge = timeit.timeit(lambda: merge_sort(data.copy()), number=3)
        print(f"{size:<15} | {'Merge Sort':<20} | {t_merge:<25.6f}")

        # Тест Timsort (вбудований sorted)
        t_timsort = timeit.timeit(lambda: sorted(data), number=3)
        print(f"{size:<15} | {'Timsort (sorted)':<20} | {t_timsort:<25.6f}")
        print("-" * 65)

    # Окремий тест на частково відсортованому масиві
    print("\n--- Тест на частково відсортованому масиві (розмір 10 000 елементів) ---")
    sorted_data = list(range(10000))
    
    t_merge_sorted = timeit.timeit(lambda: merge_sort(sorted_data.copy()), number=5)
    t_timsort_sorted = timeit.timeit(lambda: sorted(sorted_data), number=5)
    
    print(f"Merge Sort на відсортованому: {t_merge_sorted:.6f} сек.")
    print(f"Timsort на відсортованому:    {t_timsort_sorted:.6f} сек. (значно швидше завдяки адаптивності)")

if __name__ == "__main__":
    run_benchmarks()