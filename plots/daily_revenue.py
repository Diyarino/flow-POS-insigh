"""
Module for daily revenue analysis and visualization.

This module provides tools to aggregate transaction data by date and 
generate high-quality line plots suitable for reports and publications.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


def plot_daily_revenue(df: pd.DataFrame, date_col: str = 'Datum_Tag', 
                       amount_col: str = 'Bruttobetrag') -> plt.Figure:
    """
    Analyze daily revenue and return a Matplotlib figure.

    Groups the data by the specified date column, calculates the sum of 
    revenue, and formats a line plot with appropriate date formatting.

    Args:
        df (pd.DataFrame): The input transaction data.
        date_col (str): Name of the column containing dates (datetime objects).
            Defaults to 'Datum_Tag'.
        amount_col (str): Name of the column containing revenue values.
            Defaults to 'Bruttobetrag'.

    Returns:
        plt.Figure: The generated Matplotlib figure object.

    Raises:
        KeyError: If the specified columns are not found in the DataFrame.
    """
    
    # Aggregate revenue by date
    daily_revenue = df.groupby(date_col)[amount_col].sum()

    # Create figure and axes objects for professional control
    fig, ax = plt.subplots(figsize=(6, 3))
    
    # Plotting logic
    ax.plot(
        daily_revenue.index, 
        daily_revenue.values, 
        marker='o', 
        linestyle='-', 
        color='#1f77b4', 
        lw=1, 
        markersize=3
    )
    
    # Styling and labels
    ax.set_title('Daily Revenue Trend')
    ax.set_xlabel('Date')
    ax.set_ylabel('Revenue (€)')
    
    # Format x-axis to show day and month (e.g., 15.03)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
    
    ax.grid(True, linestyle='--', alpha=0.7)
    fig.tight_layout()
    
    return fig


if __name__ == "__main__":
    # Internal test block
    print("Module 'daily_revenue_analysis' initialized.")