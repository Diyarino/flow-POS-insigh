"""
Main entry point for the Retail Analytics Dashboard.

This script orchestrates data loading, preprocessing, and the generation 
of various sales, tax, and market basket visualizations.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Import custom plot modules
from utils.config_plots import configure_plt
from plots.daily_revenue import plot_daily_revenue
from plots.top_products import plot_top_products
from plots.revenue_heatmap import plot_revenue_heatmap
from plots.weekday_distribution import plot_weekday_distribution
from plots.monthly_revenue import plot_monthly_revenue
from plots.basket_distribution import plot_basket_distribution
from plots.payment_distribution import clean_tax_column, plot_payment_distribution
from plots.tax_distribution import plot_tax_distribution
from plots.payment_heatmap import plot_payment_time_heatmap
from plots.highlights import plot_monthly_top_combinations
from plots.top_comparison import plot_top_products_comparison
from plots.product_heatmap import plot_hourly_product_heatmap

# Import reporting modules
from print.combination_report import get_top_item_combinations, print_combination_report
from print.time_window import analyze_time_window, print_time_window_report

# --- CONFIGURATION ---
DATA_PATH = '/media/diyar/3387c237-bd78-4cd3-adc5-e25c4ce87fa4/datasets/cash_register_system/raw/Einzelumsätze_2026-02-17_14-50-03.xlsx'
OUTPUT_DIR = 'output'
SAVE_PLOTS = False  # Set to True to auto-save files


def load_and_preprocess_data(file_path: str) -> pd.DataFrame:
    """
    Loads the Excel sales data and performs initial feature engineering.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found at: {file_path}")

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Loading data...")
    df = pd.read_excel(file_path)

    # Feature Engineering
    df['Belegdatum'] = pd.to_datetime(df['Belegdatum'])
    df['Monat_Zahl'] = df['Belegdatum'].dt.month
    df['Datum_Tag'] = df['Belegdatum'].dt.date
    df['Monat_Name'] = df['Belegdatum'].dt.month_name()
    
    # Custom cleaning from payment module
    df['Steuersatz_Clean'] = clean_tax_column(df)

    return df


def run_visualizations(df: pd.DataFrame):
    """
    Generates and optionally saves all analytical plots.
    """
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Generating visualizations...")
    
    plots = {
        "daily_revenue.png": plot_daily_revenue(df),
        "top_products.png": plot_top_products(df, top_n=10),
        "revenue_heatmap.png": plot_revenue_heatmap(df),
        "weekday_variance.png": plot_weekday_distribution(df),
        "monthly_trend.png": plot_monthly_revenue(df),
        "basket_distribution.png": plot_basket_distribution(df, limit=50.0),
        "payment_methods.png": plot_payment_distribution(df),
        "tax_distribution.png": plot_tax_distribution(df),
        "payment_time_analysis.png": plot_payment_time_heatmap(df),
        "basket_top_analysis.png": plot_monthly_top_combinations(
            df, receipt_col='BelegID (intern)', item_col='Artikel'
        ),
        "product_heatmap.png": plot_hourly_product_heatmap(df),
        "product_comparison.png": plot_top_products_comparison(df)
    }

    if SAVE_PLOTS:
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        for filename, fig in plots.items():
            fig.savefig(os.path.join(OUTPUT_DIR, filename), dpi=300)
            print(f"Saved {filename}")

    plt.show()


def run_reports(df: pd.DataFrame):
    """
    Calculates and prints textual reports to the console.
    """
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Generating text reports...")
    
    # Market Basket Analysis
    top_pairs = get_top_item_combinations(df, top_n=10)
    print_combination_report(top_pairs)

    # Closing Time Analysis
    closing_stats = analyze_time_window(df, start_h=20, start_m=45, end_h=21, end_m=0)
    print_time_window_report(closing_stats)


def main():
    """
    Main orchestration logic.
    """
    configure_plt()

    try:
        # Step 1: Data
        df = load_and_preprocess_data(DATA_PATH)

        # Step 2: Visuals
        run_visualizations(df)

        # Step 3: Text Reports
        run_reports(df)

        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Analysis complete.")

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")


if __name__ == "__main__":
    main()