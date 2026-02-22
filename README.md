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

We hypothesize that timsort will outperform both insertion and merge sort for all 
values of n in terms of wall clock execution speed when the optimal value of k is used.  
We expect that the optimal value of k will be close to the crossover point found in Q5, 
in the range of 50 to 75, though it may differ slightly since the hybrid sort calls 
insertion sort on subarrays within a recursive context rather than on independent arrays.

### Methods

The hybrid sorting algorithm, `timsort`, uses the standard merge sort recursive structure but switches to an insertion sort pass whenever the partition size drops to or below a threshold size `k`. 

To determine the optimal value of `k`, two separate search strategies were implemented and compared on a randomly generated array of size $n=10000$:
1. **Cross-Validation Approach:** We tested every multiple of 5 between $k = 5$ and $k = 500$ ($k \in \{5, 10, 15... 500\}$). For each $k$, `timsort` was run 10 times using the `time` module on fresh copies of the array, and the $k$ producing the lowest total time was recorded as optimal.
2. **Ternary Search Approach:** Because the runtime function of a sorting algorithm with respect to `k` forms a unimodal (U-shaped) curve, we implemented a ternary search algorithm to find the absolute minimum runtime. This search recursively discarded one-third of the search space (initially $k=1$ to $k=1000$) by comparing exactly two midpoints (`time` repetitions = 25) until the optimal threshold `k` was isolated.  
   * **Note on Ternary Search for Timsort:** While ternary search is theoretically optimal for continuous unimodal functions, Timsort's runtime with respect to `k` actually forms a step-function with flat plateaus. Because the array is recursively halved, the base case array sizes only exist at specific integer boundaries (e.g., sizes 19, 20, 39, 40). Thus, a threshold of $k=20$ and $k=38$ will trigger the exact same execution path and the exact same number of insertion sorts for an array of size 39. This creates flat plateaus on the runtime curve. Ternary search struggles on these plateaus because it relies on strictly decreasing/increasing slopes to narrow the search space; on a flat plateau, micro-fluctuations in hardware execution time will cause it to arbitrarily discard sections of the search space, leading to variance in the exact identified optimal $k$.

To ensure statistical significance, both search methods pre-generated the same list of 10 deterministic random arrays. This allowed the algorithms to compute the true average runtime across the 10 data distributions for each tested $k$ without adding random data variance during the searches. The results of both searches were plotted using `matplotlib` to visually confirm the runtime curves and optimal threshold.

Finally, using the optimal $k$ derived from the searches, `timsort` was directly compared against standalone `insertion_sort` and `merge_sort`. The performance of all three algorithms was evaluated and recorded across arrays of varying sizes (from $n=5$ to $n=10000$) to determine the most efficient sorting strategy for different input scales.

Additional details:
1. Language: Python 3.12.5
2. Timing: using `time` module
3. Input: randomly generated arrays of size 10000
4. Number of repetitions per k: 25 for both cross validation and ternary search
5. Source Code: https://github.com/robrosk/sorting_comparison

### Results

Cross validation results:
Best k: 10, 15, 20

Ternary search results:
Best k: 12, 16, 18, 23, 28, 31

Across all array sizes n from 5 to 10000, timsort was faster than merge sort and insertion sort.  The difference between timsort and insertion sort was minimal as the size of n grew.

### Discussion

**What is the optimal k?**
Based on our empirical testing using both cross-validation and ternary search across 10 deterministic randomly generated arrays, the optimal value for the threshold `k` was consistently found to be in the range of `k = 10` to `k = 33`, with cross-validation strongly indicating `k = 10` to `k = 20`. 

**Is k the same as the crossover point from Q5? Why or why not?**
No, the optimal `k` is strictly smaller than the crossover point found in Q5 ($n \approx 50$ to $75$). This discrepancy exists because Q5 tested Insertion Sort and Merge Sort as *standalone* algorithms operating on completely independent arrays. 

In Timsort, Insertion Sort is called recursively continuously at the bottom of the Merge Sort execution tree. While Insertion Sort on its own might remain faster than a full Merge Sort algorithm up to $n=75$, in the hybrid context, doing an insertion sort on a subarray of size 75 takes significantly longer than simply letting Merge Sort perform one or two more recursive splits down to arrays of size 15-20 before using Insertion Sort. The overhead of the recursive calls for sizes 20-75 is actually *less* than the quadratic time penalty $O(n^2)$ incurred by forcing Insertion Sort to handle those larger subarrays manually. Therefore, the optimal time to switch to Insertion Sort in a hybrid environment happens earlier (at a smaller $n$) than the breakeven point of the two standalone algorithms.

### Conclusion

The results strongly support our hypothesis that Timsort, when utilizing an optimized `k` threshold (in our case, tightly bound around $10 \le k \le 30$), outperforms both standalone Insertion Sort and standalone Merge Sort across all input sizes. The optimization strategy, bolstered by analyzing the step-function plateau nature of Timsort's recursive halving, confirms that integrating a fast $O(n^2)$ algorithm at the leaves of an $O(n \log n)$ divide-and-conquer tree yields the most historically successful and highly performant sorting architecture.  Although our hypothesis was supported related to the relative performance of timsort vs insertion sort and merge sort, the optimal k value was found to be smaller than the crossover point found in Q5 ($n \approx 50$ to $75$).

