import pandas as pd
import itertools
import os
import time
import multiprocessing
from tqdm import tqdm
import plotly.graph_objects as go

def load_transactions(file_path='data/transactions.csv'):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
    if 'client_id' not in df.columns or 'product' not in df.columns:
        raise ValueError("The dataset must contain columns 'client_id' and 'product'.")
    transactions = df.groupby('client_id')['product'].apply(list).tolist()
    return transactions

def generate_candidates(transactions):
    itemsets = set()
    for transaction in tqdm(transactions, desc="Generating candidates"):
        unique_items = set(transaction)
        if len(unique_items) >= 2:
            for pair in itertools.combinations(sorted(unique_items), 2):
                itemsets.add(pair)
    return list(itemsets)

def count_support_chunk(chunk, candidates):
    """
    Partial support counting for a chunk of transactions.
    Returns a dictionary with partial counts.
    """
    local_counts = {c: 0 for c in candidates}
    for transaction in chunk:
        unique_items = set(transaction)
        for pair in candidates:
            if pair[0] in unique_items and pair[1] in unique_items:
                local_counts[pair] += 1
    return local_counts

def count_support_parallel(transactions, candidates, num_processes=2):
    """
    Splits transactions into 'num_processes' chunks and uses multiprocessing.Pool
    to count support in parallel.
    """
    pool = multiprocessing.Pool(processes=num_processes)

    # Divide transactions into chunks
    chunk_size = len(transactions) // num_processes
    chunks = []
    start = 0
    for i in range(num_processes):
        end = start + chunk_size
        # For the last chunk, take the remainder
        if i == num_processes - 1:
            end = len(transactions)
        chunks.append(transactions[start:end])
        start = end

    # Parallel mapping of counting function
    partial_counts = pool.starmap(count_support_chunk, [(chunk, candidates) for chunk in chunks])
    pool.close()
    pool.join()

    # Combine partial counts
    total_counts = {c: 0 for c in candidates}
    for pcount in partial_counts:
        for c in pcount:
            total_counts[c] += pcount[c]

    # Convert counts to support
    total_transactions = len(transactions)
    support = {c: total_counts[c] / total_transactions for c in candidates}
    return support

def benchmark(transactions, candidates, process_list=[1,2,3,4,6]):
    """
    Measures the execution time of count_support_parallel using different numbers of processes.
    Returns a dictionary {num_processes: time_taken}.
    """
    times = {}
    for num in process_list:
        start_time = time.time()
        _ = count_support_parallel(transactions, candidates, num_processes=num)
        end_time = time.time()
        times[num] = end_time - start_time
        print(f"Processes={num} -> Time={times[num]:.4f} s")
    return times

def plot_benchmark(times, output_path='plots/benchmarking_plot.png'):
    """
    Generates a simple plot of number of processes vs. execution time and saves it as a .png file.
    """
    x = list(times.keys())
    y = list(times.values())

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name='Time (s)'))
    fig.update_layout(
        title="Parallel Support Counting Benchmark",
        xaxis_title="Number of Processes",
        yaxis_title="Time (s)",
        template="plotly_white"
    )
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.write_image(output_path)
    print(f"Benchmark plot saved in {output_path}")

def main():
    # Load transactions
    transactions = load_transactions()
    # Generate candidate 2-itemsets
    candidates = generate_candidates(transactions)

    # Example: Count support in parallel using 4 processes
    support_dict = count_support_parallel(transactions, candidates, num_processes=4)
    
    # Filter frequent itemsets based on a minimum support threshold
    min_support = 0.01
    frequent_itemsets = {k: v for k, v in support_dict.items() if v >= min_support}

    # Save frequent itemsets to CSV
    os.makedirs("results", exist_ok=True)
    with open("results/frequent_itemsets.csv", "w", encoding="utf-8") as f:
        f.write("itemset,support\n")
        for itemset, sup in frequent_itemsets.items():
            f.write(f"{itemset},{sup:.4f}\n")

    # Benchmark the parallel counting using different process counts and generate a plot
    process_list = [1, 2, 3, 4, 6]
    times = benchmark(transactions, candidates, process_list=process_list)
    plot_benchmark(times)

if __name__ == "__main__":
    main()