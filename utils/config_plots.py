"""
Module for Matplotlib configuration.

This module provides utility functions to standardize the appearance of 
plots, including optional LaTeX rendering and font management.
"""

import shutil
import matplotlib.pyplot as plt


def configure_plt(check_latex=True):
    """
    Configures Matplotlib global parameters for professional plotting.

    Sets font sizes, title sizes, and attempts to enable LaTeX rendering 
    if the necessary tools are installed on the system.

    Args:
        check_latex (bool): If True, the function checks for a local LaTeX 
            installation (via 'latex' command) before enabling usetex. 
            Defaults to True.

    Returns:
        None

    Notes:
        - If LaTeX is found, it uses 'Times New Roman' as the serif font.
        - If LaTeX is not found, it falls back to standard serif fonts.
        - Disables 'figure.max_open_warning' to avoid console clutter.
    """
    
    # Check for LaTeX availability and configure rendering
    if check_latex and shutil.which('latex'):
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif', serif=['Times New Roman'])
    else:
        plt.rc('text', usetex=False)
        plt.rc('font', family='serif')
    
    # Global Plot Parameters
    plt.rcParams.update({
        'figure.max_open_warning': 0,
        'font.size': 12,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.autolayout': True  # Ensures labels aren't cut off
    })


if __name__ == "__main__":
    # This block allows testing the configuration directly
    configure_plt()
    print("Matplotlib has been configured successfully.")