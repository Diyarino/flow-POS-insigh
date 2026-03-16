"""
Module for hourly sales distribution analysis.

This module provides tools to visualize product sales density over 
different hours of the day using heatmaps.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_hourly_product_heatmap(
    df: pd.DataFrame, 
    item_col: str = 'Artikel', 
    hour_col: str = 'Stunde', 
    qty_col: str = 'Menge',
    top_n: int = 15
) -> plt.Figure:
    """
    Analyze hourly sales distribution for top products and return a heatmap.

    Args:
        df (pd.DataFrame): The input transaction data.
        item_col (str): Column name for product names.
        hour_col (str): Column name for the hour of sale.
        qty_col (str): Column name for the quantity sold.
        top_n (int): Number of top products to include in the heatmap.

    Returns:
        plt.Figure: The generated Matplotlib figure object.
    """
    
    # 1. Data Cleaning & Filtering
    df_clean = df.copy()
    df_clean[hour_col] = pd.to_numeric(df_clean[hour_col], errors='coerce').fillna(0).astype(int)
    
    # Restrict to relevant business hours (10:00 - 23:00)
    df_filtered = df_clean[(df_clean[hour_col] >= 10) & (df_clean[hour_col] <= 23)]

    # 2. Identify Top Products
    top_products = df_filtered.groupby(item_col)[qty_col].sum().nlargest(top_n).index
    df_top = df_filtered[df_filtered[item_col].isin(top_products)]

    # 3. Create Pivot Table
    pivot_table = df_top.pivot_table(
        index=item_col, 
        columns=hour_col, 
        values=qty_col, 
        aggfunc='sum'
    ).fillna(0)

    # Sort items by total volume for better visualization
    item_order = pivot_table.sum(axis=1).sort_values(ascending=False).index
    pivot_table = pivot_table.reindex(item_order)

    # 4. Plotting
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(
        pivot_table, 
        cmap='YlOrRd', 
        linewidths=.5, 
        annot=True, 
        fmt='g',
        ax=ax
    )

    ax.set_title(f'Heatmap: Hourly Product Sales (Top {top_n})', fontsize=14, fontweight='bold')
    ax.set_xlabel('Hour of Day (24h)')
    ax.set_ylabel('Product Name')

    fig.tight_layout()
    
    return fig


if __name__ == "__main__":
    print("Module 'hourly_analysis' initialized.")