"""
Module for Market Basket Analysis (Association Analysis).

This module identifies frequently co-purchased items (product pairs) 
from transaction data to optimize menu bundles and cross-selling.
"""

from collections import Counter
from itertools import combinations
import pandas as pd


def get_top_item_combinations(df: pd.DataFrame, 
                              receipt_id_col: str = 'BelegID (intern)', 
                              item_col: str = 'Artikel', 
                              top_n: int = 10) -> list:
    """
    Identify the most frequent pairs of items bought together.

    Groups the items by receipt, generates all unique pairs within 
    each receipt, and counts their global frequency.

    Args:
        df (pd.DataFrame): The input transaction data.
        receipt_id_col (str): Column identifying unique receipts. 
            Defaults to 'BelegID (intern)'.
        item_col (str): Column name for product names. 
            Defaults to 'Artikel'.
        top_n (int): Number of top combinations to return. 
            Defaults to 10.

    Returns:
        list: A list of tuples containing ((item1, item2), count), 
            sorted by frequency.
    """
    
    # 1. Group items by receipt into lists
    # We drop NaN values and convert everything to string for consistency
    baskets = (
        df.groupby(receipt_id_col)[item_col]
        .apply(list)
    )

    pair_counter = Counter()

    # 2. Iterate through each basket and find combinations
    for items in baskets:
        # Clean items: remove NaNs and sort to avoid (A,B) vs (B,A) duplicates
        cleaned_items = sorted([
            str(item) for item in items 
            if pd.notna(item) and str(item).lower() != 'nan'
        ])
        
        # Only process baskets with at least two items
        if len(cleaned_items) >= 2:
            # Update counter with unique pairs (combinations of 2)
            pair_counter.update(combinations(cleaned_items, 2))

    return pair_counter.most_common(top_n)


def print_combination_report(top_combinations: list) -> None:
    """
    Format and print the market basket results to the console.

    Args:
        top_combinations (list): The output from get_top_item_combinations.
    """
    print(f"\n{'='*50}")
    print(f"{'TOP COMBINATIONS (Frequently Bought Together)':^50}")
    print(f"{'='*50}")
    
    for (item1, item2), count in top_combinations:
        print(f" {item1:20} + {item2:20} | {count:>5} times")
    
    print(f"{'='*50}\n")


if __name__ == "__main__":
    print("Module 'market_basket_analysis' initialized.")