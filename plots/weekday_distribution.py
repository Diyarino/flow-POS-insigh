"""
Module for weekday-based revenue distribution analysis.

This module provides tools to analyze the variance and distribution of 
daily revenue across different days of the week using boxplots.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_weekday_distribution(df: pd.DataFrame, 
                              day_col: str = 'Wochentag', 
                              date_col: str = 'Datum_Tag',
                              value_col: str = 'Bruttobetrag') -> plt.Figure:
    """
    Create a boxplot showing the distribution of revenue per weekday.

    First aggregates the data to get total revenue per unique date, 
    then visualizes the spread for each weekday to identify trends 
    and outliers.

    Args:
        df (pd.DataFrame): The input transaction data.
        day_col (str): Column name for weekdays. Defaults to 'Wochentag'.
        date_col (str): Column name for unique dates. Defaults to 'Datum_Tag'.
        value_col (str): Column name for revenue values. Defaults to 'Bruttobetrag'.

    Returns:
        plt.Figure: Matplotlib figure object containing the boxplot.
    """
    
    # Define chronological order for German weekdays
    weekday_order = [
        'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 
        'Freitag', 'Samstag', 'Sonntag'
    ]

    # 1. Data Processing: Sum revenue per day and weekday
    # This ensures we plot the distribution of "Daily Totals"
    daily_totals = (
        df.groupby([date_col, day_col])[value_col]
        .sum()
        .reset_index()
    )

    # 2. Visualization
    fig, ax = plt.subplots(figsize=(8, 4))
    
    sns.boxplot(
        data=daily_totals,
        x=day_col, 
        y=value_col, 
        order=weekday_order, 
        hue=day_col, 
        palette="Set3", 
        legend=False,
        ax=ax
    )
    
    # Styling
    ax.set_title('Risk Analysis: Revenue Variance by Weekday', fontsize=14)
    ax.set_ylabel('Daily Revenue (€)')
    ax.set_xlabel('Weekday')
    
    # Add a subtle grid for better readability of the values
    ax.grid(True, axis='y', linestyle='--', alpha=0.5)
    
    fig.tight_layout()
    
    return fig


if __name__ == "__main__":
    print("Module 'weekday_analysis' initialized.")