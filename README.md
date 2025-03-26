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
   - Saves the results in `results/frequent_itemsets.csv`.

2. **Parallel Version (`src/parallel_version.py`)**  
   - Divides transactions into chunks and uses `multiprocessing.Pool` for parallel support counting.  
   - Benchmarks execution times using 1, 2, 3, 4, and 6 processes.  
   - Generates a plot in `plots/benchmarking_plot.png`.

3. **Performance Analysis (`src/parallel_version_with_subplots.py`)**  
   - Compares serial vs parallel execution.  
   - Computes and plots **real vs ideal speedup**.  
   - Saves results in `plots/performance_analysis.png`.

4. **Main Script (`main.py`)**  
   - Automates the process: runs the serial version, the parallel version, and the performance analysis.  
   - Output files are automatically generated.

---

## 4. How to Run the Project

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the main script
Execute the following command from the project root:
```bash
python main.py
```

### 3. Check the output files
- `results/frequent_itemsets.csv`: Contains the frequent itemsets with support ≥ `min_support`.
- `plots/benchmarking_plot.png`: Shows execution time vs number of processes.
- `plots/performance_analysis.png`: Shows combined performance analysis (serial vs parallel execution and speedup).

---

## 5. Benchmark Results

### ⏱️ Execution Time (Actual Results)

| Number of Processes | Time (s) |
|---------------------|----------|
| 1                   | 0.0874   |
| 2                   | 0.0660   |
| 3                   | 0.0668   |
| 4                   | 0.0574   |
| 6                   | 0.0655   |

### 📊 Top Frequent Itemsets (support ≥ 0.04)

| Itemset                       | Support |
|------------------------------|---------|
| ('Product_16', 'Product_2')  | 0.0425  |
| ('Product_16', 'Product_9')  | 0.0425  |
| ('Product_16', 'Product_3')  | 0.0424  |
| ('Product_15', 'Product_7')  | 0.0421  |
| ('Product_13', 'Product_16') | 0.0421  |
| ('Product_16', 'Product_18') | 0.0420  |
| ('Product_16', 'Product_5')  | 0.0420  |
| ('Product_4', 'Product_6')   | 0.0418  |
| ('Product_0', 'Product_8')   | 0.0418  |
| ('Product_16', 'Product_17') | 0.0418  |

> 🔍 Total of 133 itemsets found with support above the threshold. See `results/frequent_itemsets.csv` for full list.

---

## 6. Conclusions

- ✅ **The parallel version significantly improves execution time over the serial version.**
- ⚠️ **Adding more processes eventually leads to diminishing returns due to overhead.**
- 💡 **This project demonstrates the effectiveness of parallel computing for scalable data mining.**

---

## 📁 Repository Structure

```plaintext
parallel-frequent-itemset-mining/
├── main.py
├── requirements.txt
├── .gitignore
├── README.md
├── data/
│   └── transactions.csv
├── results/
│   └── frequent_itemsets.csv
├── plots/
│   ├── benchmarking_plot.png
│   └── performance_analysis.png
└── src/
|   ├── serial_version.py
|   ├── parallel_version.py
|   ├── parallel_version_with_subplots.py
|   ├── performance_plots.py
|   └── utils.py
|
└── README.md
```


## 👥 Made by

- Alan Mendoza  
- Daniel Herrera  
- Frank Chan  
- Rogelio Novelo  
- Krishna Sandoval  
- Emmanuel Carmona  
- Carlos Helguera
