"""
Module for customer basket analysis (Average Transaction Value).

This module visualizes the distribution of receipt totals to understand 
customer spending behavior and average order values.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_basket_distribution(df: pd.DataFrame, 
                             receipt_col: str = 'Belegnummer', 
                             amount_col: str = 'Bruttobetrag',
                             limit: float = 50.0) -> plt.Figure:
    """
    Analyze and plot the distribution of receipt totals.

    Calculates the sum per receipt, filters for 'normal' transaction sizes 
    to improve visualization, and marks the global mean.

    Args:
        df (pd.DataFrame): The input transaction data.
        receipt_col (str): Column identifying unique receipts. 
            Defaults to 'Belegnummer'.
        amount_col (str): Column for transaction amounts. 
            Defaults to 'Bruttobetrag'.
        limit (float): Upper limit for the x-axis to filter outliers for 
            the plot. Defaults to 50.0.

    Returns:
        plt.Figure: Matplotlib figure object containing the histogram.
    """
    
    # 1. Data Processing: Calculate total value per unique receipt
    basket_values = df.groupby(receipt_col)[amount_col].sum()
    
    # Calculate the true mean before filtering for the plot
    true_mean = basket_values.mean()
    
    # Filter values for better histogram visualization
    basket_filtered = basket_values[basket_values <= limit]

    # 2. Visualization
    fig, ax = plt.subplots(figsize=(8, 4))
    
    sns.histplot(
        basket_filtered, 
        bins=20, 
        kde=True, 
        color='green', 
        ax=ax,
        edgecolor='white'
    )
    
    # Add vertical line for the average
    ax.axvline(
        true_mean, 
        color='red', 
        linestyle='--', 
        label=f'Average: {true_mean:.2f}€'
    )
    
    # Styling
    ax.set_title('Customer Spending Distribution (Basket Size)', fontsize=14, pad=15)
    ax.set_xlabel('Receipt Amount (€)')
    ax.set_ylabel('Number of Orders')
    ax.set_xlim(0, limit)
    
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    
    fig.tight_layout()
    
    return fig


if __name__ == "__main__":
    print("Module 'basket_analysis' initialized.")