# Hypothesis

I hypothesize that insertion sort will outperform merge sort for small input sizes due to its lower constant overhead.  Insertion sort has no recursion or extra memory allocation.  I expect the crossover point to be around n = 50 to 200, after which merge sorts $O(nlog(n))$ growth rate will dominate insertion sorts $O(n^2)$ growth rate.

# Methods

1. Language: Python 3.12.5
2. Timing: using `timeit` module
3. Input: randomly generated arrays, and generating fresh random arrays for each test so neither algorithm gets pre-sorted data.
4. Range of n values tested (n = 5, 10, 20, 50, 75, 100, 125, 150, 175, 200, 500, 1000, 2500, 5000, 10000)
5. Number of repetitions per n to get stable averages: 10
6. Source Code: https://github.com/robrosk/sorting_comparison

# Results

| Array Size (n) | Insertion Sort Time (s) | Merge Sort Time (s) | Faster Algorithm |
| :--- | :--- | :--- | :--- |
| 5 | 0.000001 | 0.000002 | Insertion Sort |
| 10 | 0.000001 | 0.000004 | Insertion Sort |
| 20 | 0.000004 | 0.000009 | Insertion Sort |
| 50 | 0.000018 | 0.000025 | Insertion Sort |
| 75 | 0.000043 | 0.000040 | Merge Sort |
| 100 | 0.000066 | 0.000056 | Merge Sort |
| 125 | 0.000104 | 0.000069 | Merge Sort |
| 150 | 0.000143 | 0.000086 | Merge Sort |
| 175 | 0.000202 | 0.000101 | Merge Sort |
| 200 | 0.000263 | 0.000115 | Merge Sort |
| 500 | 0.001791 | 0.000339 | Merge Sort |
| 1000 | 0.007855 | 0.000676 | Merge Sort |
| 2500 | 0.052306 | 0.001959 | Merge Sort |
| 5000 | 0.222814 | 0.004283 | Merge Sort |
| 10000 | 0.873973 | 0.009378 | Merge Sort |

**Finding**: Merge sort first became faster than insertion sort at **n = 75**.

# Discussion



