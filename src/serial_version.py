import pandas as pd
import itertools
import os
from tqdm import tqdm

def load_transactions(file_path='data/transactions.csv'):
    """
    Loads a CSV file containing transactions.
    The file must have columns: 'client_id' and 'product'.
    Returns:
      - transactions (list of lists): Each element is a list of products purchased in a transaction.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()

    if 'client_id' not in df.columns or 'product' not in df.columns:
        raise ValueError("The dataset must contain columns 'client_id' and 'product'.")

    # Group products by client
    transactions = df.groupby('client_id')['product'].apply(list).tolist()
    return transactions

def generate_candidates(transactions):
    """
    Generates all possible pairs (2-itemsets) from transactions.
    Returns a unique list of pairs.
    """
    itemsets = set()
    for transaction in tqdm(transactions, desc="Generating candidates"):
        unique_items = set(transaction)
        if len(unique_items) >= 2:
            for pair in itertools.combinations(sorted(unique_items), 2):
                itemsets.add(pair)
    return list(itemsets)

def count_support_serial(transactions, candidates):
    """
    Counts the support of each 2-itemset sequentially.
    Returns a dictionary { itemset: support }.
    """
    counts = {itemset: 0 for itemset in candidates}
    total_transactions = len(transactions)

    for transaction in tqdm(transactions, desc="Counting support (serial)"):
        unique_items = set(transaction)
        for pair in candidates:
            if pair[0] in unique_items and pair[1] in unique_items:
                counts[pair] += 1

    # Convert counts to support by dividing by the total number of transactions
    support = {itemset: counts[itemset] / total_transactions for itemset in counts}
    return support

def main():
    # Load transactions
    transactions = load_transactions()

    # Generate candidate 2-itemsets
    candidates = generate_candidates(transactions)

    # Count support (serial version)
    support_dict = count_support_serial(transactions, candidates)
    
    # Filter by a minimum support threshold
    min_support = 0.01
    frequent_itemsets = {k: v for k, v in support_dict.items() if v >= min_support}

    # Save the frequent itemsets to a CSV file
    os.makedirs("results", exist_ok=True)
    with open("results/frequent_itemsets.csv", "w", encoding="utf-8") as f:
        f.write("itemset,support\n")
        for itemset, sup in frequent_itemsets.items():
            f.write(f"{itemset},{sup:.4f}\n")

    print("Frequent itemsets saved in 'results/frequent_itemsets.csv'.")

if __name__ == "__main__":
    main()