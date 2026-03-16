"""
Module for comparing sales trends of top products.

This module visualizes the intraday sales volume for the most popular 
items to identify peak performance times.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_top_products_comparison(
    df: pd.DataFrame, 
    item_col: str = 'Artikel', 
    hour_col: str = 'Stunde', 
    qty_col: str = 'Menge',
    top_limit: int = 3
) -> plt.Figure:
    """
    Compare the hourly sales trend of the top N products.

    Args:
        df (pd.DataFrame): The input transaction data.
        item_col (str): Column name for product names.
        hour_col (str): Column name for the hour of sale.
        qty_col (str): Column name for the quantity sold.
        top_limit (int): Number of top products to compare. Defaults to 3.

    Returns:
        plt.Figure: The generated Matplotlib figure object.
    """
    
    # 1. Identify top N products based on total quantity
    top_items = df.groupby(item_col)[qty_col].sum().nlargest(top_limit).index
    df_top_subset = df[df[item_col].isin(top_items)]

    # 2. Plotting Logic
    fig, ax = plt.subplots(figsize=(7, 4))
    
    sns.lineplot(
        data=df_top_subset, 
        x=hour_col, 
        y=qty_col, 
        hue=item_col, 
        estimator='sum', 
        errorbar=None, 
        marker='o',
        ax=ax
    )

    # Styling and Labels
    ax.set_title(f'Intraday Trend: Top {top_limit} Products', fontsize=14, fontweight='bold')
    ax.set_xlabel('Hour of Day (24h)')
    ax.set_ylabel('Total Quantity Sold')
    
    # Ensure x-axis shows every relevant hour
    ax.set_xticks(range(int(df_top_subset[hour_col].min()), int(df_top_subset[hour_col].max()) + 1))
    
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(title='Product', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    fig.tight_layout()
    
    return fig


if __name__ == "__main__":
    print("Module 'product_comparison' initialized.")