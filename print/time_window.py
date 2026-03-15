"""
Module for specific time window performance analysis.

This module provides tools to filter transactions within a custom 
time range and calculate key performance indicators (KPIs) like 
total revenue and average ticket size for that period.
"""

from datetime import time
import pandas as pd


def analyze_time_window(df: pd.DataFrame, 
                        start_h: int = 20, start_m: int = 45,
                        end_h: int = 21, end_m: int = 0,
                        date_col: str = 'Belegdatum',
                        amount_col: str = 'Bruttobetrag') -> dict:
    """
    Analyze sales KPIs for a specific time window.

    Filters the dataframe for a given start and end time and calculates 
    the number of receipts, total revenue, and average revenue.

    Args:
        df (pd.DataFrame): The input transaction data.
        start_h (int): Start hour. Defaults to 20.
        start_m (int): Start minute. Defaults to 45.
        end_h (int): End hour. Defaults to 21.
        end_m (int): End minute. Defaults to 0.
        date_col (str): Column name for the timestamp. Defaults to 'Belegdatum'.
        amount_col (str): Column name for the revenue. Defaults to 'Bruttobetrag'.

    Returns:
        dict: A dictionary containing 'count', 'total_revenue', and 'average'.
    """
    
    # 1. Ensure datetime format and define time objects
    df[date_col] = pd.to_datetime(df[date_col])
    start_time = time(start_h, start_m)
    end_time = time(end_h, end_m)

    # 2. Filter data using a mask
    mask = (df[date_col].dt.time >= start_time) & (df[date_col].dt.time <= end_time)
    filtered_df = df.loc[mask].copy()

    # 3. Clean revenue column if necessary
    if filtered_df[amount_col].dtype == object:
        filtered_df[amount_col] = (
            filtered_df[amount_col]
            .astype(str)
            .str.replace(',', '.', regex=False)
            .astype(float)
        )

    # 4. Calculate KPIs
    results = {
        'start': start_time,
        'end': end_time,
        'count': len(filtered_df),
        'total_revenue': filtered_df[amount_col].sum(),
        'average': filtered_df[amount_col].mean()
    }

    return results


def print_time_window_report(results: dict) -> None:
    """
    Print a professional summary of the time window analysis.
    """
    print(f"\n{'='*50}")
    print(f"{'TIME WINDOW PERFORMANCE REPORT':^50}")
    print(f"{'='*50}")
    print(f" Period:        {results['start']} - {results['end']}")
    print(f" Total Receipts: {results['count']}")
    print(f" Total Revenue:  {results['total_revenue']:,.2f} €")
    print(f" Avg. Receipt:   {results['average']:,.2f} €")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    print("Module 'time_window_analysis' initialized.")