import os
import pandas as pd
import itertools
from tqdm import tqdm

# Import the performance module to generate the plots
from performance_plots import main as performance_main

# Import the functions from the serial and parallel versions
from serial_version import count_support_serial
from parallel_version import count_support_parallel

def load_transactions(file_path='data/transactions.csv'):
    """
    Loads the CSV file containing transactions.
    The file must have the columns 'client_id' and 'product'.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
    if 'client_id' not in df.columns or 'product' not in df.columns:
        raise ValueError("The dataset must contain the columns 'client_id' and 'product'.")
    transactions = df.groupby('client_id')['product'].apply(list).tolist()
    return transactions

def generate_candidates(transactions):
    """
    Generates all 2-itemsets from the transactions.
    """
    itemsets = set()
    for transaction in tqdm(transactions, desc="Generating candidates"):
        unique_items = set(transaction)
        if len(unique_items) >= 2:
            for pair in itertools.combinations(sorted(unique_items), 2):
                itemsets.add(pair)
    return list(itemsets)

if __name__ == "__main__":
    # Load data
    transactions = load_transactions()
    candidates = generate_candidates(transactions)
    
    performance_main(
    func_serial=count_support_serial,
    func_parallel=count_support_parallel,
    transactions=transactions,
    candidates=candidates,
    process_list=[1, 2, 3, 4, 6],
    output_path="plots/performance_analysis.png"
)
    
    print("Done! Check 'plots/analisis_rendimiento.png' to see the performance plots.")
