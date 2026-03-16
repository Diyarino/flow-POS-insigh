"""
Module for monthly market basket analysis and visualization.

This module identifies the most frequent product pairs per month and 
visualizes them in a professional bar chart for retail insights.
"""

from collections import Counter
from itertools import combinations
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_monthly_top_combinations(
    df: pd.DataFrame, 
    receipt_col: str = 'BelegID (intern)', 
    item_col: str = 'Artikel',
    month_idx_col: str = 'Monat_Zahl',
    month_name_col: str = 'Monat_Name'
) -> plt.Figure:
    """
    Analyze the top product pair per month and return a Matplotlib figure.

    Groups data by month and transaction ID to find the most frequent 
    co-occurrences of product pairs.

    Args:
        df (pd.DataFrame): The input transaction data.
        receipt_col (str): Column identifying unique transactions.
        item_col (str): Column containing item names.
        month_idx_col (str): Column with month numbers (1-12).
        month_name_col (str): Column with month names (e.g., 'Januar').

    Returns:
        plt.Figure: The generated Matplotlib figure object.
    """
    
    monthly_highlights = []

    # 1. Data Analysis Logic
    for month_idx in range(1, 13):
        df_month = df[df[month_idx_col] == month_idx]

        if df_month.empty:
            continue

        # Group items by receipt and count pairs
        receipts = df_month.groupby(receipt_col)[item_col].apply(list)
        pair_counter = Counter()

        for article_list in receipts:
            # Clean: Remove nans, unique items only, and sort for consistency
            items = sorted(list(set(
                [str(x) for x in article_list if str(x).lower() != 'nan']
            )))

            if len(items) >= 2:
                pair_counter.update(combinations(items, 2))

        if pair_counter:
            top_pair, count = pair_counter.most_common(1)[0]
            month_name = df_month[month_name_col].iloc[0]

            monthly_highlights.append({
                'Month_No': month_idx,
                'Month': month_name,
                'Combination': f"{top_pair[0]} +\n{top_pair[1]}",
                'Sales': count
            })

    res_df = pd.DataFrame(monthly_highlights).sort_values('Month_No')

    # 2. Plotting Logic
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.set_style("whitegrid")

    sns.barplot(
        data=res_df,
        x='Month',
        y='Sales',
        hue='Month',
        palette='viridis',
        legend=False,
        ax=ax
    )

    # Styling and Annotations
    ax.set_title('Top Monthly Product Combinations', fontsize=14, fontweight='bold')
    ax.set_ylabel('Co-occurrence Count')
    ax.set_xlabel('Month')
    plt.xticks(rotation=45)

    # Add labels on top of bars
    for i, row in res_df.iterrows():
        # Get position based on the categorical axis
        x_pos = list(res_df['Month']).index(row['Month'])
        
        ax.text(
            x_pos, 
            row['Sales'] + 0.2, 
            row['Combination'], 
            ha='center', 
            va='bottom', 
            fontsize=8, 
            fontweight='bold',
            bbox=dict(facecolor='white', alpha=0.6, edgecolor='none', boxstyle='round')
        )

    fig.tight_layout()
    
    return fig


if __name__ == "__main__":
    # Internal test block
    print("Module 'market_basket_analysis' initialized.")