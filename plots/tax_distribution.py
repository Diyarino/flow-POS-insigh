"""
Module for tax-related sales distribution analysis.

This module provides tools to visualize the quantity of items sold 
at different tax rates (e.g., 7% vs 19%), helping to distinguish 
between food/take-away and drinks/dine-in sales.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_tax_distribution(df: pd.DataFrame, 
                          tax_col: str = 'Steuersatz_Clean', 
                          qty_col: str = 'Menge') -> plt.Figure:
    """
    Visualize the quantity of items sold by tax rate.

    Aggregates the total quantity per tax rate and generates a bar chart 
    with descriptive labels and data annotations on top of the bars.

    Args:
        df (pd.DataFrame): The input dataframe (must contain cleaned tax rates).
        tax_col (str): Column name for cleaned tax floats. Defaults to 'Steuersatz_Clean'.
        qty_col (str): Column name for quantities sold. Defaults to 'Menge'.

    Returns:
        plt.Figure: Matplotlib figure object containing the tax distribution plot.
    """
    
    # 1. Data Processing: Sum quantity by tax rate
    tax_dist = df.groupby(tax_col)[qty_col].sum()

    # Create descriptive labels based on common German tax rules
    labels = []
    for rate in tax_dist.index:
        if rate == 7.0:
            labels.append('7% (Food / Take-away)')
        elif rate == 19.0:
            labels.append('19% (Drinks / Dine-in)')
        else:
            labels.append(f'{rate}% (Other)')

    # 2. Visualization
    fig, ax = plt.subplots(figsize=(8, 4))
    
    # Create the barplot
    sns.barplot(
        x=labels, 
        y=tax_dist.values, 
        hue=labels, 
        palette='pastel', 
        legend=False,
        ax=ax
    )
    
    # Styling
    ax.set_title('Items Sold by Tax Rate / Category', fontsize=14, pad=15)
    ax.set_ylabel('Total Items Sold')
    ax.set_xlabel('Tax Rate / Category')
    
    # Add values on top of bars
    for i, value in enumerate(tax_dist.values):
        ax.text(
            i, value, f'{int(value)}', 
            ha='center', va='bottom', 
            fontweight='bold', fontsize=10
        )
    
    # Polish the layout
    fig.tight_layout()
    
    return fig


if __name__ == "__main__":
    print("Module 'tax_analysis' initialized.")