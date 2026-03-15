"""
Module for product performance analysis and visualization.

This module contains tools to identify best-selling items and 
visualize them using categorical plots.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_top_products(df: pd.DataFrame, item_col: str = 'Artikel', 
                      qty_col: str = 'Menge', top_n: int = 10) -> plt.Figure:
    """
    Identify top-selling products and return a horizontal bar chart.

    Aggregates the total quantity sold per item, sorts them, and creates
    a Seaborn barplot for the top N products.

    Args:
        df (pd.DataFrame): The input transaction data.
        item_col (str): Column name for product names. Defaults to 'Artikel'.
        qty_col (str): Column name for quantities sold. Defaults to 'Menge'.
        top_n (int): Number of top products to display. Defaults to 10.

    Returns:
        plt.Figure: Matplotlib figure object containing the bar chart.
    """
    
    # 1. Data Processing: Calculate top products
    top_products = (
        df.groupby(item_col)[qty_col]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
    )

    # 2. Visualization
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(6, 3))
    
    # Create the barplot
    sns.barplot(
        x=top_products.values, 
        y=top_products.index, 
        hue=top_products.index, 
        palette='viridis', 
        legend=False,
        ax=ax  # Explicitly tell Seaborn to use our created axis
    )
    
    # Styling
    ax.set_title(f'Top {top_n} Bestsellers (by Quantity)')
    ax.set_xlabel('Quantity Sold')
    ax.set_ylabel('Product Name')
    
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    
    # Adjust layout to prevent long product names from being cut off
    fig.tight_layout()
    
    return fig


if __name__ == "__main__":
    print("Module 'product_analysis' initialized.")