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
def plot_results(results):
    k_values = results[:, 0]
    times = results[:, 1]
    plt.plot(k_values, times)
    plt.xlabel("k")
    plt.ylabel("Time (s)")
    plt.title("Timsort Performance")
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

    return results, best_k, best_time

# find optimal k value
def find_optimal_k(arr, k_values):
    results, best_k, best_time = cross_validation(arr, k_values)

    # np array for ease of use
    results = np.array(results)
    # plot results
    plot_results(results)

    return best_k, best_time

def main():
    array_size = 10000
    seed = int(input("Enter a random seed for the arrays: "))

    arr = generate_random_array(array_size, seed)

    k_values = range(5, 500 + 1, 5)
    print(k_values)

    optimal_k, optimal_time = find_optimal_k(arr, k_values)

    print(f"Optimal k: {optimal_k}")
    print(f"Optimal time: {optimal_time}")

if __name__ == "__main__":
    main()