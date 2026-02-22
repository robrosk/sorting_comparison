from insertion_sort import insertion_sort
from merge_sort import merge
from generate_data import generate_random_array
import time
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

# evaluate wallclock time on deterministic seeds
def evaluate_timsort(arrays, k):
    total_time = 0
    num_trials = len(arrays)
    
    for arr in arrays:
        test_arr = arr.copy()
            
        start_time = time.perf_counter()
        timsort(test_arr, k)
        end_time = time.perf_counter()
        
        total_time += (end_time - start_time)
        
    time_per_trial = total_time / num_trials

    return time_per_trial

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
def cross_validation(array_size, k_values, seed=0, num_trials=10):
    best_k = None
    best_time = float('inf')
    results = []

    arrays = [generate_random_array(array_size, seed + i) for i in range(num_trials)]

    for k in k_values:
        timsort_time = evaluate_timsort(arrays, k)
        results.append((k, timsort_time))
        if timsort_time < best_time:
            best_k = k
            best_time = timsort_time
            print(f"Found new best k: {best_k} with time: {best_time}")

    results = np.array(results)
    plot_results(results, "Timsort Performance - Cross Validation Approach")

    return best_k

# ternary search to find optimal k value (lowest runtime)
def ternary_search(arrays, left, right, results):
    if right - left < 3:
        best_k = left
        best_time = float('inf')
        for k_val in range(left, right + 1):
            t = evaluate_timsort(arrays, k_val)
            results.append((k_val, t))
            if t < best_time:
                best_k = k_val
                best_time = t

        return best_k, best_time, results
    
    m1 = left + (right - left) // 3
    m2 = right - (right - left) // 3

    timsort_time_m1 = evaluate_timsort(arrays, m1)
    timsort_time_m2 = evaluate_timsort(arrays, m2)

    results.append((m1, timsort_time_m1))
    results.append((m2, timsort_time_m2))
    
    if timsort_time_m1 < timsort_time_m2:
        return ternary_search(arrays, left, m2, results)
    else:
        return ternary_search(arrays, m1, right, results)

# find optimal k value for timsort - uses ternary search
def find_optimal_k(array_size, low_k, high_k, seed=0, num_trials=25):    
    arrays = [generate_random_array(array_size, seed + i) for i in range(num_trials)]
    optimal_k, best_time, ternary_results = ternary_search(arrays, low_k, high_k, [])

    ternary_results.sort(key=lambda x: x[0])
    plot_results(ternary_results, f"Timsort Performance - Ternary Search Approach (optimal k = {optimal_k})")

    return optimal_k

def main():
    array_size = 10000
    seed = int(input("Enter a random seed for the arrays: "))

    k_values = range(5, 500 + 1, 5)

    optimal_k_cv = cross_validation(array_size, k_values, seed, num_trials=10)

    print("Cross validation results:")
    print(f"Best k: {optimal_k_cv}")

    optimal_k_ternary = find_optimal_k(array_size, low_k=1, high_k=1000, seed=seed, num_trials=10)

    print("Ternary search results:")
    print(f"Best k: {optimal_k_ternary}")

    same_result = abs(optimal_k_cv - optimal_k_ternary) <= 5
    print(f"Ternary search found nearly the same optimal k as cross validation: {same_result}")

if __name__ == "__main__":
    main()