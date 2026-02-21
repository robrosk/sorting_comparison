from generate_data import generate_random_array
import timeit

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

def main():
    n_values = [5, 10, 20, 50, 75, 100, 125, 150, 175, 200, 500, 1000, 2500, 5000, 10000]
    first_faster_n = None
        for n in n_values:
            arr = generate_random_array(n, 42)
            insertion_time = timeit.timeit(lambda: insertion_sort(arr.copy()), number=10)
            merge_time = timeit.timeit(lambda: merge_sort(arr.copy()), number=10)
        print(f"n = {n}: Insertion Sort = {insertion_time / 10:.6f}s, Merge Sort = {merge_time / 10:.6f}s")
            
            if first_faster_n is None and merge_time < insertion_time:
                first_faster_n = n

        if first_faster_n is not None:
        print(f"\nMerge sort first became faster than insertion sort at n = {first_faster_n}")
        else:
        print("\nMerge sort never became faster than insertion sort in this test.")

if __name__ == "__main__":
    main()