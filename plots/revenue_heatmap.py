"""
Module for temporal business analysis.

This module provides tools to visualize peak hours and sales patterns 
using heatmaps, helping to identify the busiest times of the week.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_revenue_heatmap(df: pd.DataFrame, 
                         day_col: str = 'Wochentag', 
                         hour_col: str = 'Stunde', 
                         value_col: str = 'Bruttobetrag') -> plt.Figure:
    """
    Create a heatmap of revenue distributed by weekday and hour.

    Aggregates the total revenue into a pivot table and visualizes it 
    to show peak business hours. Handles sorting of German weekdays.

    Args:
        df (pd.DataFrame): The input transaction data.
        day_col (str): Column name for weekdays. Defaults to 'Wochentag'.
        hour_col (str): Column name for hours. Defaults to 'Stunde'.
        value_col (str): Column name for revenue values. Defaults to 'Bruttobetrag'.

    Returns:
        plt.Figure: Matplotlib figure object containing the heatmap.
    """
    
    # Define the chronological order for sorting (based on your data's language)
    weekday_order = [
        'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 
        'Freitag', 'Samstag', 'Sonntag'
    ]

    # 1. Data Processing: Create the pivot table
    pivot_data = df.pivot_table(
        index=hour_col, 
        columns=day_col, 
        values=value_col, 
        aggfunc='sum'
    )

    # Reindex to ensure Monday-Sunday order and filter only existing days
    existing_days = [day for day in weekday_order if day in pivot_data.columns]
    pivot_data = pivot_data.reindex(columns=existing_days)

    # 2. Visualization
    fig, ax = plt.subplots(figsize=(8, 6))
    
    sns.heatmap(
        pivot_data, 
        cmap='coolwarm', 
        annot=False, 
        linewidths=.5, 
        ax=ax,
        cbar_kws={'label': 'Total Revenue (€)'}
    )
    
    # Styling
    ax.set_title('Revenue Heatmap: Peak Business Hours', fontsize=14, pad=15)
    ax.set_ylabel('Hour of Day')
    ax.set_xlabel('Weekday')
    
    fig.tight_layout()
    
    return fig


if __name__ == "__main__":
    print("Module 'hourly_analysis' initialized.")