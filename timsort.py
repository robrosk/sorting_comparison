from comparison import insertion_sort, merge 
from generate_data import generate_random_array
import timeit
import numpy as np
import matplotlib.pyplot as plt

# combination of merge and insertion sort based on the threshold value k
def timsort(arr, k):
    if len(arr) <= 1:
        return arr
    if len(arr) <= k:
        return insertion_sort(arr)

    mid = len(arr) // 2
    left = timsort(arr[:mid], k)
    right = timsort(arr[mid:], k)
    return merge(left, right)

# plotting with matplotlib
def plot_results(results, title):
    # make sure results is a numpy array
    results = np.array(results)

    # separate k values and times
    k_values = results[:, 0]
    times = results[:, 1]

    # plot results
    plt.plot(k_values, times)
    plt.xlabel("k values")
    plt.ylabel("Time (s)")
    plt.title(title)
    plt.show()

# cross validation approach to find optimal k value
def cross_validation(arr, k_values):
    best_k = None
    best_time = float('inf')

    results = []

    for k in k_values:
        timsort_time = timeit.timeit(lambda: timsort(arr.copy(), k), number=10)
        results.append((k, timsort_time))
        if timsort_time < best_time:
            best_k = k
            best_time = timsort_time
            print(f"Found new best k: {best_k} with time: {best_time}")

    results = np.array(results)
    plot_results(results, "Timsort Performance - Cross Validation Approach")

    return results, best_k, best_time

# ternary search to find optimal k value (lowest runtime)
def ternary_search(arr, left, right, results):
    if right - left < 3:
        final_time = timeit.timeit(lambda: timsort(arr.copy(), left), number=25)
        results.append((left, final_time))
        return left, final_time, results
    
    m1 = left + (right - left) // 3
    m2 = right - (right - left) // 3

    timsort_time_m1 = timeit.timeit(lambda: timsort(arr.copy(), m1), number=25)
    timsort_time_m2 = timeit.timeit(lambda: timsort(arr.copy(), m2), number=25)

    results.append((m1, timsort_time_m1))
    results.append((m2, timsort_time_m2))
    
    if timsort_time_m1 < timsort_time_m2:
        return ternary_search(arr, left, m2, results)
    else:
        return ternary_search(arr, m1, right, results)

# find optimal k value for timsort
def find_optimal_k(arr, k_values):
    results, optimal_k_cv, best_time_cv = cross_validation(arr, k_values)

    print("Cross validation results:")
    print(f"Best k: {optimal_k_cv}")
    print(f"Best time: {best_time_cv}")

    optimal_k_ternary, best_time_ternary, ternary_results = ternary_search(arr, 1, 5000, [])
    ternary_results.sort(key=lambda x: x[0])
    
    plot_results(ternary_results, "Timsort Performance - Ternary Search Approach")

    print("Ternary search results:")
    print(f"Best k: {optimal_k_ternary}")
    print(f"Best time: {best_time_ternary}")

    same_result = (optimal_k_cv == optimal_k_ternary) and (best_time_cv == best_time_ternary)
    print(f"Ternary search found the same optimal k and best time as cross validation: {same_result}")


def main():
    array_size = 10000
    seed = int(input("Enter a random seed for the arrays: "))

    arr = generate_random_array(array_size, seed)

    k_values = range(5, 500 + 1, 5)

    find_optimal_k(arr, k_values)

if __name__ == "__main__":
    main()