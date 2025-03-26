import pandas as pd
import itertools
import os
from tqdm import tqdm

def load_transactions(file_path='data/transactions.csv'):

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
    Generates all possible 2-itemsets from the transactions.
    Returns a unique list of itemsets.
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

    # Convert counts to support by dividing by total number of transactions
    support = {itemset: counts[itemset] / total_transactions for itemset in counts}
    return support

def main():
    transactions = load_transactions()
    candidates = generate_candidates(transactions)
    support_dict = count_support_serial(transactions, candidates)
    
    min_support = 0.01  # example threshold
    frequent_itemsets = {k: v for k, v in support_dict.items() if v >= min_support}

    os.makedirs("results", exist_ok=True)
    with open("results/frequent_itemsets.csv", "w", encoding="utf-8") as f:
        f.write("itemset,support\n")
        for itemset, sup in frequent_itemsets.items():
            f.write(f"{itemset},{sup:.4f}\n")

    print("Frequent itemsets saved to 'results/frequent_itemsets.csv'.")

if __name__ == "__main__":
    main()
