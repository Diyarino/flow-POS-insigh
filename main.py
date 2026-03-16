import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations
from collections import Counter

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


from print.combination_report import get_top_item_combinations, print_combination_report
from print.time_window import analyze_time_window, print_time_window_report

# %%

configure_plt()

# %% 1. Datei laden

file_path = '/media/diyar/3387c237-bd78-4cd3-adc5-e25c4ce87fa4/datasets/cash_register_system/raw/Einzelumsätze_2026-02-17_14-50-03.xlsx'

df = pd.read_excel(file_path)
df['Belegdatum'] = pd.to_datetime(df['Belegdatum'])
df['Monat_Zahl'] = df['Belegdatum'].dt.month
df['Datum_Tag'] = df['Belegdatum'].dt.date
df['Steuersatz_Clean'] = clean_tax_column(df)
df['Monat_Name'] = df['Belegdatum'].dt.month_name()

# %% plots

fig_rev = plot_daily_revenue(df)
# fig_rev.savefig('output/daily_revenue.png', dpi=300)

fig_prod = plot_top_products(df, top_n=10)
# fig_prod.savefig('output/top_products.png', dpi=300)

fig_heat = plot_revenue_heatmap(df)
# fig_heat.savefig('output/revenue_heatmap.png', dpi=300)

fig_dist = plot_weekday_distribution(df)
# fig_dist.savefig('output/weekday_variance.png', dpi=300)

fig_month = plot_monthly_revenue(df)
# fig_month.savefig('output/monthly_trend.png', dpi=300)

fig_basket = plot_basket_distribution(df, limit=50.0)
# fig_basket.savefig('output/basket_distribution.png', dpi=300)

fig_payment = plot_payment_distribution(df)
# fig_payment.savefig('output/payment_methods.png', dpi=300)

fig_tax = plot_tax_distribution(df)
# fig_tax.savefig('output/tax_distribution.png', dpi=300)

fig_pay_time = plot_payment_time_heatmap(df)
# fig_pay_time.savefig('output/payment_time_analysis.png', dpi=300)

fig_basket = plot_monthly_top_combinations(df, receipt_col='BelegID (intern)', item_col='Artikel')
# fig_basket.savefig('output/basket_top_analysis.png', dpi=300)

from hourly_analysis import plot_hourly_product_heatmap

fig_heatmap = plot_hourly_product_heatmap(df)
# fig_heatmap.savefig('output/heatmap.png', dpi=300)

plt.show()


# %% prints

top_pairs = get_top_item_combinations(df, top_n=10)
print_combination_report(top_pairs)

closing_stats = analyze_time_window(df, start_h=20, start_m=45, end_h=21, end_m=0)
print_time_window_report(closing_stats)


# %%



# %%

top_3 = top_produkte_liste[:3]
df_top3 = df[df['Artikel'].isin(top_3)]

plt.figure(figsize=(6, 3))
sns.lineplot(data=df_top3, x='Stunde', y='Menge', hue='Artikel', estimator='sum', errorbar=None, marker='o')
plt.title('Tagesverlauf der Top 3 Produkte im Vergleich')
plt.grid(True, linestyle='--', alpha=0.5)
plt.xticks(range(10, 24))
plt.ylabel('Verkaufte Menge (Summe)')
plt.show()
