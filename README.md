# Parallel Frequent Itemset Mining

## 1. Introduction
Market Basket Analysis is used to discover frequent purchasing patterns in large transaction datasets. This project implements a support counting method for 2-itemsets (pairs of products) using both a serial and a parallel approach with Python’s multiprocessing.

## 2. Problem Description
Given a dataset of transactions, the goal is to:
- Generate all possible pairs of products (2-itemsets).
- Calculate the support (frequency) of each pair.
- Filter out pairs that do not meet a minimum support threshold (`min_support`).

## 3. Approach
1. **Serial Version (`src/serial_version.py`)**  
   - Loads the dataset (`data/transactions.csv`).
   - Generates 2-itemsets from transactions.
   - Counts support for each pair sequentially.

2. **Parallel Version (`src/parallel_version.py`)**  
   - Divides transactions into chunks and uses `multiprocessing.Pool` for parallel support counting.
   - Benchmarks execution times using 1, 2, 3, 4, and 6 processes.
   - Generates a plot (saved in `plots/benchmarking_plot.png`) showing the execution time versus the number of processes.

## 4. Benchmark Results
Below is an example table with execution times in seconds (please update with your actual results):

| Number of Processes | Time (s) |
|---------------------|----------|
| 1                   | 12.45    |
| 2                   | 7.98     |
| 3                   | 5.82     |
| 4                   | 5.10     |
| 6                   | 4.35     |

## 5. Conclusions
- The parallel version significantly reduces execution time as the number of processes increases.
- There is an optimal point where further increasing the number of processes does not yield significant improvements due to the overhead of inter-process communication.
- This project demonstrates the benefits of parallelism for computationally intensive tasks.

---

**Repository Structure:**

```plaintext
parallel-frequent-itemset-mining/
├── src/
│   ├── serial_version.py
│   ├── parallel_version.py
│   └── utils.py
├── data/
│   └── transactions.csv
├── plots/
│   └── benchmarking_plot.png
├── results/
│   └── frequent_itemsets.csv
└── README.md


## Made by Alan Mendoza, Daniel Herrera, Frank chan , Rogelio Novelo, Krishna Sandoval, Emmanuel Carmona, Carlos Helguera.
