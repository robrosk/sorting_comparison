from generate_data import generate_random_array
from insertion_sort import insertion_sort
from merge_sort import merge_sort
from timsort import timsort, find_optimal_k
import timeit

import numpy as np
import matplotlib.pyplot as plt

def merge_versus_insertion():
    n_values = [5, 10, 20, 50, 75, 100, 125, 150, 175, 200, 500, 1000, 2500, 5000, 10000]
    first_faster_n = None
    for n in n_values:
        arr = generate_random_array(n, 42)
        insertion_time = timeit.timeit(lambda: insertion_sort(arr.copy()), number=10) / 10
        merge_time = timeit.timeit(lambda: merge_sort(arr.copy()), number=10) / 10
        print(f"n = {n}: Insertion Sort = {insertion_time:.6f}s, Merge Sort = {merge_time:.6f}s")
            
        if first_faster_n is None and merge_time < insertion_time:
            first_faster_n = n
    

    if first_faster_n is not None:
        print(f"\nMerge sort first became faster than insertion sort at n = {first_faster_n}")
    else:
        print("\nMerge sort never became faster than insertion sort in this test.")

def plot_results(results):
    results = np.array(results)
    n_values = results[:, 0]
    insertion_times = results[:, 1]
    merge_times = results[:, 2]
    timsort_times = results[:, 3]
    plt.plot(n_values, insertion_times, label="Insertion Sort")
    plt.plot(n_values, merge_times, label="Merge Sort")
    plt.plot(n_values, timsort_times, label="Timsort")
    plt.xlabel("n values (array size)")
    plt.ylabel("Time (s)")
    plt.title("Comparison of Sorting Algorithms")
    plt.legend()
    plt.show()

def timsort_versus_merge_and_insertion():
    n_values = [5, 10, 20, 50, 75, 100, 125, 150, 175, 200, 500, 1000, 2500, 5000, 10000]
    results = []

    seed = int(input("Enter a random seed for the arrays: "))
    print()

    k = find_optimal_k(10000, 1, 1000, seed)
    print(f"Optimal k: {k}\n")

    for n in n_values:
        arr = generate_random_array(n, seed)
        insertion_time = timeit.timeit(lambda: insertion_sort(arr.copy()), number=10) / 10
        merge_time = timeit.timeit(lambda: merge_sort(arr.copy()), number=10) / 10
        timsort_time = timeit.timeit(lambda: timsort(arr.copy(), k), number=10) / 10
        print(f"n = {n}: Insertion Sort = {insertion_time:.6f}s, Merge Sort = {merge_time:.6f}s, Timsort = {timsort_time:.6f}s")
        results.append((n, insertion_time, merge_time, timsort_time))
    
    plot_results(results)


# compares merge and insertion sort - separately compares timsort to both and graphs all three
def main():
    # Q5
    print("Merge versus Insertion Sort...\n")
    merge_versus_insertion()
    print("\nMerge versus Insertion Sort Complete...\n")

    # Q6
    print("Timsort versus Insertion Sort versus Merge Sort...\n")
    timsort_versus_merge_and_insertion()
    print("\nTimsort versus Insertion Sort versus Merge Sort Complete...\n")


if __name__ == "__main__":
    main()