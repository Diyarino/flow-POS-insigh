"""
Module for monthly business performance analysis.

This module provides functions to aggregate sales data by month and 
visualize the annual revenue trend using bar charts with data labels.
"""

import matplotlib.pyplot as plt
import pandas as pd


def plot_monthly_revenue(df: pd.DataFrame, 
                         month_col: str = 'Monat_Zahl', 
                         value_col: str = 'Bruttobetrag') -> plt.Figure:
    """
    Create a bar chart showing total revenue for each month.

    Aggregates the revenue by month number, creates a bar chart, and 
    automatically annotates each bar with its total value.

    Args:
        df (pd.DataFrame): The input transaction data.
        month_col (str): Column name for month numbers (1-12). 
            Defaults to 'Monat_Zahl'.
        value_col (str): Column name for revenue values. 
            Defaults to 'Bruttobetrag'.

    Returns:
        plt.Figure: Matplotlib figure object containing the monthly bar chart.
    """
    
    # 1. Data Processing: Calculate total revenue per month
    monthly_revenue = df.groupby(month_col)[value_col].sum()

    # 2. Visualization
    fig, ax = plt.subplots(figsize=(8, 4))
    
    # Create the bars
    bars = ax.bar(
        monthly_revenue.index, 
        monthly_revenue.values, 
        color='#e74c3c', 
        edgecolor='black', 
        alpha=0.8
    )
    
    # Styling
    ax.set_title('Annual Performance: Total Revenue per Month', fontsize=14, pad=15)
    ax.set_xlabel('Month (1=Jan, 12=Dec)')
    ax.set_ylabel('Total Revenue (€)')
    
    # Ensure all months (1-12) are shown on the x-axis
    ax.set_xticks(range(1, 13))
    
    # Add a light grid for the y-axis
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    # Professional way to add labels on top of bars
    ax.bar_label(bars, padding=3, fmt='%.0f€', fontsize=9)
    
    # Adjust layout to prevent clipping of labels
    fig.tight_layout()
    
    return fig


if __name__ == "__main__":
    print("Module 'monthly_analysis' initialized.")