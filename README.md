# Sorting Experiments

This repository contains two separate experiments that analyze the performance characteristics of different sorting algorithms:

1. **Experiment 1 (Q5):** Compares the performance of pure Insertion Sort and Merge Sort based on the size of the array. The goal is to establish the wall-clock time crossover point where the $O(n \log n)$ growth rate of Merge Sort overtakes the $O(n^2)$ growth rate of Insertion Sort.
2. **Experiment 2 (Q6):** Analyzes the performance of a hybrid sorting algorithm (a simplified Timsort) that uses Merge Sort recursively but switches to Insertion Sort when the partition size drops to or below a threshold $k$. The goal is to determine the optimal value for $k$, investigate whether this optimal $k$ differs from the standalone crossover point found in Q5 due to recursive overhead, and compare the overall performance of the hybrid approach against both pure algorithms across various input sizes.

## Q5: Insertion Sort vs Merge Sort

### Hypothesis

I hypothesize that insertion sort will outperform merge sort for small input sizes due to its lower constant overhead.  Insertion sort has no recursion or extra memory allocation.  I expect the crossover point to be around n = 50 to 200, after which merge sorts $O(nlog(n))$ growth rate will dominate insertion sorts $O(n^2)$ growth rate.

### Methods

1. Language: Python 3.12.5
2. Timing: using `timeit` module
3. Input: randomly generated arrays, and generating fresh random arrays for each test so neither algorithm gets pre-sorted data.
4. Range of n values tested (n = 5, 10, 20, 50, 75, 100, 125, 150, 175, 200, 500, 1000, 2500, 5000, 10000)
5. Number of repetitions per n to get stable averages: 10
6. Source Code: https://github.com/robrosk/sorting_comparison

### Results

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

### Discussion

I found that merge sort was faster than insertion sort for all values of $n \geq 75$.  This is consistent with my hypothesis, as the crossover point fell at the lower end of my predicted range of 50 to 200.  Between $n = 50$ and $n = 75$, the two algorithms were nearly indistinguishable, with insertion sort holding a very slight edge.  Beyond the crossover, the gap grew dramatically. By $n = 10000$, insertion sort was roughly 93 times slower than merge sort, clearly illustrating the difference between $O(n^2)$ and $O(n \log n)$ growth rates.  Because the time difference is so small near the crossover, the practical advantage of insertion sort is limited to very small inputs.  One limitation of this experiment is that only randomly generated arrays were tested.  Nearly sorted input would likely favor insertion sort further, potentially shifting the crossover point higher.  Additionally, only 10 repetitions were used per input size, which may introduce some variance in the timing results, particularly at small values of n where execution times are in the microseconds.

### Conclusion

Under the conditions tested, insertion sort had faster wall clock time for $n \leq 50$, while merge sort had faster wall clock time for $n \geq 75$.  For $n$ between 50 and 75, the two algorithms were essentially indistinguishable.  The practical advantage of insertion sort is limited to very small inputs, while merge sort is the clear winner for larger inputs.

---

## Q6: Timsort Analysis

### Hypothesis

We hypothesize that timsort will outperform both insertion and merge sort for all values of n in terms of wall clock execution speed when the optimal value of k is used.  We expect that the optimal value of k will match the crossover point found in Q5, being within the range of 50 to 75.  

### Methods

1. Language: Python 3.12.5
2. Timing: using `timeit` module
3. Input: randomly generated arrays of size n
4. Range of n values tested: 0 to 10000
5. Number of repetitions per n: 10
6. Source Code: https://github.com/robrosk/sorting_comparison

### Results



### Discussion


### Conclusion

