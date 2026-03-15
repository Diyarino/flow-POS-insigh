"""
Module for analyzing payment method preferences over time.

This module provides tools to visualize the relationship between the 
hour of the day and the chosen payment method using heatmaps.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_payment_time_heatmap(df: pd.DataFrame, 
                              hour_col: str = 'Stunde', 
                              method_col: str = 'Zahlart') -> plt.Figure:
    """
    Create a heatmap showing payment method frequency by hour.

    Uses a crosstab to count how many times each payment method was used 
    at each hour of the day.

    Args:
        df (pd.DataFrame): The input transaction data.
        hour_col (str): Column name for the hour. Defaults to 'Stunde'.
        method_col (str): Column name for the payment method. 
            Defaults to 'Zahlart'.

    Returns:
        plt.Figure: Matplotlib figure object containing the heatmap.
    """
    
    # 1. Data Processing: Create a frequency table (crosstab)
    heatmap_data = pd.crosstab(df[hour_col], df[method_col])

    # 2. Visualization
    fig, ax = plt.subplots(figsize=(7, 6))
    
    sns.heatmap(
        heatmap_data, 
        cmap="YlGnBu", 
        annot=True, 
        fmt='d', 
        ax=ax,
        cbar_kws={'label': 'Number of Receipts'}
    )
    
    # Styling
    ax.set_title('Payment Method Usage by Hour', fontsize=14, pad=15)
    ax.set_xlabel('Payment Method')
    ax.set_ylabel('Hour of Day')
    
    fig.tight_layout()
    
    return fig


if __name__ == "__main__":
    print("Module 'payment_time_analysis' initialized.")