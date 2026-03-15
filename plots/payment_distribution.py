"""
Module for payment method and tax rate analysis.

This module provides tools to clean tax-related string data and 
visualize the revenue share of different payment methods.
"""

import matplotlib.pyplot as plt
import pandas as pd


def clean_tax_column(df: pd.DataFrame, column_name: str = 'Steuersatz') -> pd.Series:
    """
    Cleans a tax rate string column and converts it to float.

    Handles percentages, non-breaking spaces, and European decimal commas.

    Args:
        df (pd.DataFrame): The input dataframe.
        column_name (str): The name of the tax column. Defaults to 'Steuersatz'.

    Returns:
        pd.Series: A cleaned float series of the tax rates.
    """
    return (
        df[column_name]
        .astype(str)
        .str.replace('%', '', regex=False)
        .str.replace('\xa0', '', regex=False)
        .str.replace(' ', '', regex=False)
        .str.replace(',', '.', regex=False)
        .astype(float)
    )


def plot_payment_distribution(df: pd.DataFrame, 
                              method_col: str = 'Zahlart', 
                              amount_col: str = 'Bruttobetrag') -> plt.Figure:
    """
    Analyze revenue share by payment method and return a donut chart.

    Args:
        df (pd.DataFrame): The input transaction data.
        method_col (str): Column for payment methods (e.g., Cash, Card).
            Defaults to 'Zahlart'.
        amount_col (str): Column for revenue values.
            Defaults to 'Bruttobetrag'.

    Returns:
        plt.Figure: Matplotlib figure object containing the donut chart.
    """
    
    # 1. Data Processing: Calculate revenue per payment method
    payment_revenue = df.groupby(method_col)[amount_col].sum()

    # 2. Visualization
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Custom colors for a professional look
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#bcbd22']
    
    # Create the pie chart
    wedges, texts, autotexts = ax.pie(
        payment_revenue, 
        labels=payment_revenue.index, 
        autopct='%1.1f%%', 
        startangle=140, 
        colors=colors[:len(payment_revenue)],
        pctdistance=0.85,  # Move percentages further out
        explode=[0.05] * len(payment_revenue)  # Slight separation
    )

    # Draw a white circle in the middle to make it a donut
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)

    # Styling texts
    plt.setp(autotexts, size=10, weight="bold", color="black")
    plt.setp(texts, size=12)
    
    ax.set_title('Revenue Share by Payment Method', fontsize=14, pad=20)
    
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.axis('equal')  
    
    fig.tight_layout()
    
    return fig


if __name__ == "__main__":
    print("Module 'payment_analysis' initialized.")