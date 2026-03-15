import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import time
from itertools import combinations
from collections import Counter

from utils.config_plots import configure_plt
from plots.daily_revenue import plot_daily_revenue
from plots.top_products import plot_top_products

# %%

configure_plt()

# %% 1. Datei laden

file_path = '/media/diyar/3387c237-bd78-4cd3-adc5-e25c4ce87fa4/datasets/cash_register_system/raw/Einzelumsätze_2026-02-17_14-50-03.xlsx'

df = pd.read_excel(file_path)
df['Belegdatum'] = pd.to_datetime(df['Belegdatum'])
df['Datum_Tag'] = df['Belegdatum'].dt.date

# %% daily_revenue_report

# --- Run Daily Revenue Analysis ---
fig_rev = plot_daily_revenue(df)
# fig_rev.savefig('output/daily_revenue.pdf')

# --- Run Product Analysis ---
fig_prod = plot_top_products(df, top_n=10)
# fig_prod.savefig('output/top_products.png', dpi=300)






plt.show()

# %%

# --- ANALYSE 3: Heatmap der Stoßzeiten (Wochentag vs. Stunde) ---
wochentage_order = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
pivot_data = df.pivot_table(index='Stunde', columns='Wochentag', values='Bruttobetrag', aggfunc='sum')

pivot_data = pivot_data.reindex(columns=[d for d in wochentage_order if d in pivot_data.columns])

plt.figure(figsize=(6, 6))
sns.heatmap(pivot_data, cmap='coolwarm', annot=False, linewidths=.5)
plt.title('Umsatz-Heatmap: Wann machen wir den meisten Umsatz?')
plt.ylabel('Uhrzeit (Stunde)')
plt.xlabel('Wochentag')
plt.tight_layout()
plt.show()


# %%
# Datum konvertieren
df['Belegdatum'] = pd.to_datetime(df['Belegdatum'])
df['Monat_Zahl'] = df['Belegdatum'].dt.month
df['Datum_Tag'] = df['Belegdatum'].dt.date

wochentage_order = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
tagesumsatz = df.groupby(['Datum_Tag', 'Wochentag'])['Bruttobetrag'].sum().reset_index()

plt.figure(figsize=(7, 3))
sns.boxplot(x='Wochentag', y='Bruttobetrag', data=tagesumsatz, order=wochentage_order, hue='Wochentag', palette="Set3", legend=False)
plt.title('Risiko-Analyse: Wie stark schwankt der Umsatz pro Wochentag?')
plt.ylabel('Tagesumsatz (€)')
plt.grid(True, axis='y', linestyle='--', alpha=0.5)
plt.show()

# %%

# --- ANALYSE 2: Monatsverlauf (Der "schwierigste" Monat) ---
monatsumsatz = df.groupby('Monat_Zahl')['Bruttobetrag'].sum()

plt.figure(figsize=(6, 3))
bars = plt.bar(monatsumsatz.index, monatsumsatz.values, color='#e74c3c')
plt.title('Jahresverlauf: Gesamtumsatz pro Monat')
plt.xlabel('Monat (1=Januar, 12=Dezember)')
plt.ylabel('Gesamtumsatz (€)')
plt.xticks(range(1, 13)) # Zeigt Zahlen 1 bis 12 an
plt.grid(axis='y', alpha=0.3)

# Kleines Extra: Den Umsatz über den Balken schreiben
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, f'{int(yval)}€', ha='center', va='bottom', fontsize=8)

plt.show()

# %%

# --- ANALYSE 3: Durchschnittlicher Bon (Warenkorbwert) ---
bon_werte = df.groupby('Belegnummer')['Bruttobetrag'].sum()
bon_werte_normal = bon_werte[bon_werte < 50] 

plt.figure(figsize=(6, 3))
sns.histplot(bon_werte_normal, bins=20, kde=True, color='green')
plt.title('Wie viel gibt ein Kunde durchschnittlich aus? (Verteilung)')
plt.xlabel('Rechnungsbetrag (€)')
plt.ylabel('Anzahl der Bestellungen')
plt.xlim(0,50)
plt.grid()
plt.axvline(bon_werte.mean(), color='red', linestyle='--', label=f'Durchschnitt: {bon_werte.mean():.2f}€')
plt.legend()
plt.show()



# %%

# Datenbereinigung (Sicherstellen, dass Zahlen auch Zahlen sind)
df['Steuersatz_Clean'] = (
    df['Steuersatz']
    .astype(str)
    .str.replace('%', '')
    .str.replace('\xa0', '')
    .str.replace(' ', '')
    .str.replace(',', '.')
    .astype(float)
)
zahlart_umsatz = df.groupby('Zahlart')['Bruttobetrag'].sum()

plt.figure(figsize=(4, 4))
plt.pie(zahlart_umsatz, labels=zahlart_umsatz.index, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff','#99ff99'])
plt.title('Umsatzanteil nach Zahlungsart (Wo kommt das Geld her?)')
plt.show()

#%%

# --- ANALYSE 2: Im Haus (19%) vs. Außer Haus (7%) ---
steuer_verteilung = df.groupby('Steuersatz_Clean')['Menge'].sum()
labels = []
for steuer in steuer_verteilung.index:
    if steuer == 7.0:
        labels.append('7% (Meist Speisen / Außer Haus)')
    elif steuer == 19.0:
        labels.append('19% (Getränke / Im Haus)')
    else:
        labels.append(f'{steuer}% (Sonstiges)')

plt.figure(figsize=(8, 3))
sns.barplot(x=labels, y=steuer_verteilung.values, hue=labels, palette='pastel', legend=False)
plt.title('Verkaufte Menge nach Steuersatz')
plt.ylabel('Anzahl verkaufte Artikel')
plt.xlabel('Steuersatz / Typ')

# Werte über die Balken schreiben
for i, v in enumerate(steuer_verteilung.values):
    plt.text(i, v, str(int(v)), ha='center', va='bottom', fontweight='bold')

plt.show()

# %%

heatmap_data = pd.crosstab(df['Stunde'], df['Zahlart'])

plt.figure(figsize=(6, 5))
sns.heatmap(heatmap_data, cmap="YlGnBu", annot=True, fmt='d') # fmt='d' heißt ganze Zahlen (keine Kommas)
plt.title('Wann wird welche Zahlart genutzt? (Anzahl Belege)')
plt.ylabel('Uhrzeit')
plt.xlabel('Zahlart')
plt.show()

# %%

basket = df.groupby('BelegID (intern)')['Artikel'].apply(list)
count = Counter()

for row in basket:
    row_sorted = sorted([str(x) for x in row if str(x) != 'nan']) 
    if len(row_sorted) < 2:
        continue
    count.update(combinations(row_sorted, 2))

print("--- TOP 10 KOMBINATIONEN (Was wird zusammen gekauft?) ---")
for key, value in count.most_common(10):
    print(f"{key[0]} + {key[1]}: {value} mal zusammen verkauft")


# %%

df['Belegdatum'] = pd.to_datetime(df['Belegdatum'])
start_zeit = time(20, 45) # 20:30 Uhr
end_zeit = time(21, 00)   # 21:30 Uhr
maske = (df['Belegdatum'].dt.time >= start_zeit) & (df['Belegdatum'].dt.time <= end_zeit)
gefilterte_daten = df.loc[maske]

if gefilterte_daten['Bruttobetrag'].dtype == object:
    gefilterte_daten['Bruttobetrag'] = (
        gefilterte_daten['Bruttobetrag']
        .astype(str)
        .str.replace(',', '.')
        .astype(float)
    )

umsatz_zeitraum = gefilterte_daten['Bruttobetrag'].sum()
umsatz_zeitraum_durchschnitt = gefilterte_daten['Bruttobetrag'].mean()

print(f"Anzahl Belege zwischen {start_zeit} und {end_zeit}: {len(gefilterte_daten)}")
print(f"Gesamtumsatz in diesem Zeitraum: {umsatz_zeitraum:.2f} €")
print(f"Durchschnitt in diesem Zeitraum: {umsatz_zeitraum_durchschnitt:.2f} €")


# %%

df['Belegdatum'] = pd.to_datetime(df['Belegdatum'])
df['Monat_Name'] = df['Belegdatum'].dt.month_name()
# df['Monat_Name'] = df['Belegdatum'].dt.month_name(locale='German') # Falls locale Fehler macht, nimm .dt.month_name() für Englisch
df['Monat_Zahl'] = df['Belegdatum'].dt.month

monats_highlights = []

for monat in range(1, 13):
    df_monat = df[df['Monat_Zahl'] == monat]
    
    if df_monat.empty:
        continue
    kassenbons = df_monat.groupby('BelegID (intern)')['Artikel'].apply(list)
    pair_counter = Counter()
    for artikel_liste in kassenbons:
        items = sorted(list(set([str(x) for x in artikel_liste if str(x) != 'nan'])))
        if len(items) >= 2:
            pair_counter.update(combinations(items, 2))
    
    if pair_counter:
        top_pair, anzahl = pair_counter.most_common(1)[0]
        kombi_name = f"{top_pair[0]} + {top_pair[1]}" # Zeilenumbruch für die Grafik
        monats_name = df_monat['Monat_Name'].iloc[0] # Name des Monats holen
        
        monats_highlights.append({
            'Monat_Zahl': monat,
            'Monat': monats_name,
            'Top_Kombi': kombi_name,
            'Verkäufe': anzahl
        })

ergebnis_df = pd.DataFrame(monats_highlights).sort_values('Monat_Zahl')

plt.figure(figsize=(8, 4))
sns.set_style("whitegrid")

plot = sns.barplot(
    data=ergebnis_df,    # Das 'data=' Argument muss bleiben
    x='Monat', 
    y='Verkäufe', 
    hue='Monat',         # Hier nur den Spaltennamen als Text
    palette='viridis', 
    legend=False
)

# Beschriftungen hinzufügen
plt.title('Das perfekte Kombi-Angebot für jeden Monat', fontsize=16, fontweight='bold')
plt.ylabel('Anzahl der gemeinsamen Käufe', fontsize=12)
plt.xlabel('Monat', fontsize=12)
plt.xticks(rotation=45) # Monatsnamen schräg stellen, damit sie lesbar sind

# Den Namen der Kombi direkt in/über den Balken schreiben
for index, row in ergebnis_df.iterrows():
    x_pos = list(ergebnis_df['Monat']).index(row['Monat'])
    
    plt.text(
        x_pos, 
        row['Verkäufe'] + 1, # Etwas über dem Balken
        row['Top_Kombi'], 
        ha='center', 
        va='bottom', 
        fontsize=9, 
        fontweight='bold',
        color='black',
        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.2') # Hintergrundbox für Lesbarkeit
    )

plt.tight_layout()
plt.show()

# Ausgabe als einfache Tabelle in der Konsole
print("--- DEINE MONATS-EMPFEHLUNGEN ---")
print(ergebnis_df[['Monat', 'Top_Kombi', 'Verkäufe']].to_string(index=False))


# %%

df['Stunde'] = pd.to_numeric(df['Stunde'], errors='coerce').fillna(0).astype(int)

df = df[(df['Stunde'] >= 10) & (df['Stunde'] <= 23)]

top_produkte_liste = df.groupby('Artikel')['Menge'].sum().nlargest(15).index
df_top = df[df['Artikel'].isin(top_produkte_liste)]

pivot_table = df_top.pivot_table(index='Artikel', columns='Stunde', values='Menge', aggfunc='sum')

pivot_table = pivot_table.fillna(0)

pivot_table['Gesamt'] = pivot_table.sum(axis=1)
pivot_table = pivot_table.sort_values('Gesamt', ascending=False)
pivot_table = pivot_table.drop(columns='Gesamt') # Hilfsspalte wieder löschen

plt.figure(figsize=(9, 6))
sns.heatmap(pivot_table, cmap='YlOrRd', linewidths=.5, annot=True, fmt='g')

plt.title('Hitzekarte: Wann wird welches Produkt verkauft?', fontsize=16)
plt.xlabel('Uhrzeit (Stunde)', fontsize=12)

plt.tight_layout()
plt.show()


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
