import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
from datetime import datetime
from collections import Counter
from itertools import combinations

# Verhindert aufpoppende Fenster und nutzt Vektorgrafiken für Schärfe
matplotlib.use('svg')

def main(page: ft.Page):
    # --- GRUNDEINSTELLUNGEN DER APP ---
    page.title = "Umsatz Analyse Dashboard"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    
    # Globale Variable für unseren DataFrame
    global_df = [None]

    # --- HILFSFUNKTIONEN FÜR GRAFIKEN ---
    def create_chart_card(title, fig):
        return ft.Column([
            ft.Card(
                elevation=4,
                content=ft.Container(
                    padding=20,
                    content=ft.Column([
                        ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
                        ft.Divider(height=10, color=ft.colors.GREY_300),
                        MatplotlibChart(fig, transparent=True)
                    ])
                )
            ),
            ft.Divider(height=40, color=ft.colors.BLUE_GREY_100, thickness=2) 
        ])

    # --- SEITE 2: ANALYSE DASHBOARD ---
    def build_dashboard(df):
        # 1. GANZ WICHTIG: Löscht alle alten Matplotlib-Grafiken aus dem Speicher!
        plt.close('all') 
        
        # 2. Scroll-Modus für diese Spalte
        dashboard_content = ft.Column(spacing=20, scroll=ft.ScrollMode.AUTO)
        
        # 3. Header & Zurück-Button
        header = ft.Row([
            ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: show_page_1()),
            ft.Text("Dein Analyse Dashboard", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_700)
        ])
        dashboard_content.controls.append(header)
        dashboard_content.controls.append(ft.Divider(height=20, color=ft.colors.TRANSPARENT))

        # 4. ZEIT-FILTER BEREICH
        def calculate_time_range(e):
            try:
                start_time = datetime.strptime(time_von.value, "%H:%M").time()
                end_time = datetime.strptime(time_bis.value, "%H:%M").time()
                
                mask = (df['Belegdatum'].dt.time >= start_time) & (df['Belegdatum'].dt.time <= end_time)
                gefiltert = df.loc[mask].copy()
                
                if gefiltert['Bruttobetrag'].dtype == object:
                    gefiltert['Bruttobetrag'] = gefiltert['Bruttobetrag'].astype(str).str.replace(',', '.').astype(float)
                
                umsatz = gefiltert['Bruttobetrag'].sum()
                schnitt = gefiltert['Bruttobetrag'].mean() if len(gefiltert) > 0 else 0
                
                time_result.value = f"✅ {len(gefiltert)} Belege | Gesamt: {umsatz:.2f} € | Ø Bon: {schnitt:.2f} €"
                time_result.color = ft.colors.GREEN_700
            except Exception as ex:
                time_result.value = "❌ Fehler: Bitte Format HH:MM nutzen (z.B. 20:30)"
                time_result.color = ft.colors.RED_700
            page.update()

        time_von = ft.TextField(label="Von (HH:MM)", hint_text="z.B. 20:30", width=150, border_radius=10)
        time_bis = ft.TextField(label="Bis (HH:MM)", hint_text="z.B. 21:30", width=150, border_radius=10)
        time_result = ft.Text("Ergebnis erscheint hier...", size=16, weight=ft.FontWeight.W_500)
        
        time_card = ft.Card(
            elevation=4,
            color=ft.colors.BLUE_50,
            content=ft.Container(
                padding=20,
                content=ft.Column([
                    ft.Text("⏱️ Umsatz im Zeitraum berechnen", size=18, weight=ft.FontWeight.BOLD),
                    # Row für die Felder, Button darunter
                    ft.Row([time_von, time_bis]),
                    ft.ElevatedButton("Berechnen", on_click=calculate_time_range, icon=ft.icons.CALCULATE),
                    time_result
                ])
            )
        )
        dashboard_content.controls.append(time_card)
        dashboard_content.controls.append(ft.Divider(height=30, color=ft.colors.TRANSPARENT))

        # --- DATEN VORBEREITUNG FÜR ALLE PLOTS ---
        df['Belegdatum'] = pd.to_datetime(df['Belegdatum'])
        df['Datum_Tag'] = df['Belegdatum'].dt.date
        df['Monat_Zahl'] = df['Belegdatum'].dt.month
        
        if 'Stunde' not in df.columns:
            df['Stunde'] = df['Belegdatum'].dt.hour
        else:
            df['Stunde'] = pd.to_numeric(df['Stunde'], errors='coerce').fillna(0).astype(int)

        # Sichere Monats-Namen Zuweisung (OS-unabhängig)
        monate_dict = {1:'Januar', 2:'Februar', 3:'März', 4:'April', 5:'Mai', 6:'Juni', 
                       7:'Juli', 8:'August', 9:'September', 10:'Oktober', 11:'November', 12:'Dezember'}
        df['Monat_Name'] = df['Monat_Zahl'].map(monate_dict)

        # --- GRAFIKEN ERSTELLEN ---

        # 1. Täglicher Umsatzverlauf
        fig1, ax1 = plt.subplots(figsize=(7, 3.5))
        tagesumsatz = df.groupby('Datum_Tag')['Bruttobetrag'].sum()
        ax1.plot(tagesumsatz.index, tagesumsatz.values, marker='o', linestyle='-', color='#1f77b4', lw=1, markersize=4)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.'))
        ax1.grid(True, alpha=0.5)
        ax1.set_ylabel('Umsatz (€)')
        fig1.tight_layout()
        dashboard_content.controls.append(create_chart_card("Täglicher Umsatzverlauf", fig1))

        # 2. Risiko-Analyse: Wochentage (Boxplot)
        if 'Wochentag' in df.columns:
            fig_box, ax_box = plt.subplots(figsize=(7, 3.5))
            wochentage_order = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
            tagesumsatz_wt = df.groupby(['Datum_Tag', 'Wochentag'])['Bruttobetrag'].sum().reset_index()
            sns.boxplot(x='Wochentag', y='Bruttobetrag', data=tagesumsatz_wt, order=wochentage_order, 
                        hue='Wochentag', palette="Set3", legend=False, ax=ax_box)
            ax_box.set_ylabel('Tagesumsatz (€)')
            ax_box.set_xlabel('')
            ax_box.grid(True, axis='y', linestyle='--', alpha=0.5)
            fig_box.tight_layout()
            dashboard_content.controls.append(create_chart_card("Risiko-Analyse: Umsatzschwankung pro Wochentag", fig_box))

        # 3. Jahresverlauf (Balkendiagramm Monate)
        fig_mon, ax_mon = plt.subplots(figsize=(7, 3.5))
        monatsumsatz = df.groupby('Monat_Zahl')['Bruttobetrag'].sum()
        bars = ax_mon.bar(monatsumsatz.index, monatsumsatz.values, color='#e74c3c')
        ax_mon.set_xlabel('Monat')
        ax_mon.set_ylabel('Gesamtumsatz (€)')
        ax_mon.set_xticks(range(1, 13))
        ax_mon.grid(axis='y', alpha=0.3)
        for bar in bars:
            yval = bar.get_height()
            ax_mon.text(bar.get_x() + bar.get_width()/2, yval, f'{int(yval)}€', ha='center', va='bottom', fontsize=8)
        fig_mon.tight_layout()
        dashboard_content.controls.append(create_chart_card("Jahresverlauf: Gesamtumsatz pro Monat", fig_mon))

        # 4. Top 10 Bestseller
        fig2, ax2 = plt.subplots(figsize=(7, 4))
        top_produkte = df.groupby('Artikel')['Menge'].sum().sort_values(ascending=False).head(10)
        sns.barplot(x=top_produkte.values, y=top_produkte.index, hue=top_produkte.index, palette='viridis', legend=False, ax=ax2)
        ax2.set_xlabel("Verkaufte Anzahl")
        ax2.set_ylabel("")
        ax2.grid(axis='x', alpha=0.5)
        fig2.tight_layout()
        dashboard_content.controls.append(create_chart_card("Top 10 Bestseller (nach Menge)", fig2))

        # 5. Durchschnittlicher Bon (Verteilung)
        if 'Belegnummer' in df.columns:
            fig_bon, ax_bon = plt.subplots(figsize=(7, 3.5))
            bon_werte = df.groupby('Belegnummer')['Bruttobetrag'].sum()
            bon_werte_normal = bon_werte[bon_werte < 50] 
            sns.histplot(bon_werte_normal, bins=20, kde=True, color='green', ax=ax_bon)
            ax_bon.set_xlabel('Rechnungsbetrag (€)')
            ax_bon.set_ylabel('Anzahl der Bestellungen')
            ax_bon.set_xlim(0, 50)
            ax_bon.grid(alpha=0.5)
            ax_bon.axvline(bon_werte.mean(), color='red', linestyle='--', label=f'Durchschnitt: {bon_werte.mean():.2f}€')
            ax_bon.legend()
            fig_bon.tight_layout()
            dashboard_content.controls.append(create_chart_card("Warenkorbwert: Was gibt ein Kunde aus?", fig_bon))

        # 6. Heatmap: Umsatz Wochentag vs. Stunde
        if 'Stunde' in df.columns and 'Wochentag' in df.columns:
            fig3, ax3 = plt.subplots(figsize=(7, 5))
            pivot_data1 = df.pivot_table(index='Stunde', columns='Wochentag', values='Bruttobetrag', aggfunc='sum')
            pivot_data1 = pivot_data1.reindex(columns=[d for d in wochentage_order if d in pivot_data1.columns])
            sns.heatmap(pivot_data1, cmap='coolwarm', annot=False, linewidths=.5, ax=ax3)
            ax3.set_ylabel('Uhrzeit (Stunde)')
            ax3.set_xlabel('')
            fig3.tight_layout()
            dashboard_content.controls.append(create_chart_card("Heatmap: Wann machen wir den meisten Umsatz?", fig3))

        # 7. Umsatzanteil nach Zahlungsart (Pie Chart)
        if 'Zahlart' in df.columns:
            fig_pie, ax_pie = plt.subplots(figsize=(5, 5))
            zahlart_umsatz = df.groupby('Zahlart')['Bruttobetrag'].sum()
            ax_pie.pie(zahlart_umsatz, labels=zahlart_umsatz.index, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff','#99ff99', '#ffcc99'])
            fig_pie.tight_layout()
            dashboard_content.controls.append(create_chart_card("Umsatzanteil nach Zahlungsart", fig_pie))

        # 8. Steuersatz: Im Haus vs Außer Haus
        if 'Steuersatz' in df.columns:
            df['Steuersatz_Clean'] = df['Steuersatz'].astype(str).str.replace('%', '').str.replace('\xa0', '').str.replace(' ', '').str.replace(',', '.').astype(float)
            fig4, ax4 = plt.subplots(figsize=(7, 3.5))
            steuer_verteilung = df.groupby('Steuersatz_Clean')['Menge'].sum()
            labels = []
            for steuer in steuer_verteilung.index:
                if steuer == 7.0: labels.append('7% (Außer Haus)')
                elif steuer == 19.0: labels.append('19% (Im Haus)')
                else: labels.append(f'{steuer}% (Sonstiges)')
            
            sns.barplot(x=labels, y=steuer_verteilung.values, hue=labels, palette='pastel', legend=False, ax=ax4)
            ax4.set_ylabel('Verkaufte Artikel')
            for i, v in enumerate(steuer_verteilung.values):
                ax4.text(i, v, str(int(v)), ha='center', va='bottom', fontweight='bold')
            fig4.tight_layout()
            dashboard_content.controls.append(create_chart_card("In Haus (19%) vs. Außer Haus (7%)", fig4))

        # 9. Heatmap: Zahlart vs Stunde
        if 'Zahlart' in df.columns and 'Stunde' in df.columns:
            fig_heat_z, ax_heat_z = plt.subplots(figsize=(7, 5))
            heatmap_data = pd.crosstab(df['Stunde'], df['Zahlart'])
            sns.heatmap(heatmap_data, cmap="YlGnBu", annot=True, fmt='d', ax=ax_heat_z)
            ax_heat_z.set_ylabel('Uhrzeit')
            ax_heat_z.set_xlabel('Zahlart')
            fig_heat_z.tight_layout()
            dashboard_content.controls.append(create_chart_card("Wann wird welche Zahlart genutzt?", fig_heat_z))

        # 10. Monatliche Kombi-Angebote (Barplot)
        monats_highlights = []
        for monat in range(1, 13):
            df_monat = df[df['Monat_Zahl'] == monat]
            if df_monat.empty: continue
            kassenbons = df_monat.groupby('BelegID (intern)')['Artikel'].apply(list)
            pair_counter = Counter()
            for artikel_liste in kassenbons:
                items = sorted(list(set([str(x) for x in artikel_liste if str(x) != 'nan'])))
                if len(items) >= 2: pair_counter.update(combinations(items, 2))
            
            if pair_counter:
                top_pair, anzahl = pair_counter.most_common(1)[0]
                monats_name = df_monat['Monat_Name'].iloc[0]
                monats_highlights.append({'Monat_Zahl': monat, 'Monat': monats_name, 'Top_Kombi': f"{top_pair[0]}\n+ {top_pair[1]}", 'Verkäufe': anzahl})

        if monats_highlights:
            ergebnis_df = pd.DataFrame(monats_highlights).sort_values('Monat_Zahl')
            fig_kombi, ax_kombi = plt.subplots(figsize=(8, 4.5))
            sns.barplot(data=ergebnis_df, x='Monat', y='Verkäufe', hue='Monat', palette='viridis', legend=False, ax=ax_kombi)
            ax_kombi.set_ylabel('Gemeinsame Käufe')
            ax_kombi.set_xlabel('')
            plt.setp(ax_kombi.xaxis.get_majorticklabels(), rotation=45)
            
            for index, row in ergebnis_df.iterrows():
                x_pos = list(ergebnis_df['Monat']).index(row['Monat'])
                ax_kombi.text(x_pos, row['Verkäufe'] + 0.5, row['Top_Kombi'], ha='center', va='bottom', fontsize=8, fontweight='bold',
                              bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.2'))
            fig_kombi.tight_layout()
            dashboard_content.controls.append(create_chart_card("Das perfekte Kombi-Angebot pro Monat", fig_kombi))

        # 11. Heatmap: Produkte nach Uhrzeit (Top 15)
        df_filtered = df[(df['Stunde'] >= 10) & (df['Stunde'] <= 23)]
        if not df_filtered.empty:
            top_15_liste = df_filtered.groupby('Artikel')['Menge'].sum().nlargest(15).index
            df_top = df_filtered[df_filtered['Artikel'].isin(top_15_liste)]
            pivot_prod = df_top.pivot_table(index='Artikel', columns='Stunde', values='Menge', aggfunc='sum').fillna(0)
            pivot_prod['Gesamt'] = pivot_prod.sum(axis=1)
            pivot_prod = pivot_prod.sort_values('Gesamt', ascending=False).drop(columns='Gesamt')
            
            fig_prod_heat, ax_prod_heat = plt.subplots(figsize=(8, 6))
            sns.heatmap(pivot_prod, cmap='YlOrRd', linewidths=.5, annot=True, fmt='g', ax=ax_prod_heat)
            ax_prod_heat.set_xlabel('Uhrzeit (Stunde)')
            ax_prod_heat.set_ylabel('')
            fig_prod_heat.tight_layout()
            dashboard_content.controls.append(create_chart_card("Hitzekarte: Wann wird welches Produkt verkauft?", fig_prod_heat))

        # 12. Lineplot Tagesverlauf der Top 3 Produkte
        if not df_filtered.empty and len(top_15_liste) >= 3:
            top_3 = top_15_liste[:3]
            df_top3 = df_filtered[df_filtered['Artikel'].isin(top_3)]
            fig_top3, ax_top3 = plt.subplots(figsize=(7, 3.5))
            sns.lineplot(data=df_top3, x='Stunde', y='Menge', hue='Artikel', estimator='sum', errorbar=None, marker='o', ax=ax_top3)
            ax_top3.grid(True, linestyle='--', alpha=0.5)
            ax_top3.set_xticks(range(10, 24))
            ax_top3.set_ylabel('Verkaufte Menge (Summe)')
            fig_top3.tight_layout()
            dashboard_content.controls.append(create_chart_card("Tagesverlauf der Top 3 Produkte im Vergleich", fig_top3))

        # 13. PRINTS / TEXT-ANALYSEN (Top 10 Kombinationen Gesamt)
        kombi_text = ft.Text("Lade Top Kombinationen...", size=14)
        kombi_card = ft.Card(
            elevation=4,
            content=ft.Container(
                padding=20,
                content=ft.Column([
                    ft.Text("🍔 Die 10 besten Kombinationen (Gesamt)", size=18, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    kombi_text
                ])
            )
        )
        dashboard_content.controls.append(kombi_card)

        # Berechne Top 10 Kombis
        basket = df.groupby('BelegID (intern)')['Artikel'].apply(list)
        count = Counter()
        for row in basket:
            row_sorted = sorted([str(x) for x in row if str(x) != 'nan']) 
            if len(row_sorted) >= 2:
                count.update(combinations(row_sorted, 2))
        
        kombi_string = ""
        for key, value in count.most_common(10):
            kombi_string += f"• {key[0]} + {key[1]} ({value}x zusammen verkauft)\n"
        kombi_text.value = kombi_string if kombi_string else "Nicht genug Daten für Kombinationen."

        # Seite aktualisieren
        page.controls.clear()
        page.add(dashboard_content)
        page.update()

    # --- SEITE 1: UPLOAD & START ---
    def show_page_1():
        page.controls.clear()
        
        title = ft.Text("Wähle deine Umsatz-Daten (.xlsx / .csv)", size=22, weight=ft.FontWeight.BOLD)
        status_text = ft.Text("Keine Datei ausgewählt", color=ft.colors.GREY)
        
        progress_load = ft.ProgressBar(width=300, visible=False, color=ft.colors.BLUE)
        progress_analyze = ft.ProgressBar(width=300, visible=False, color=ft.colors.GREEN)
        
        text_load = ft.Text("Lese Datei ein...", visible=False, size=12)
        text_analyze = ft.Text("Erstelle Grafiken (Dies kann kurz dauern)...", visible=False, size=12)

        def on_file_picked(e: ft.FilePickerResultEvent):
            if e.files:
                selected_file = e.files[0].path
                status_text.value = f"Ausgewählt: {e.files[0].name}"
                status_text.color = ft.colors.GREEN
                btn_start.disabled = False
                global_df[0] = selected_file
            page.update()

        file_picker = ft.FilePicker(on_result=on_file_picked)
        page.overlay.append(file_picker)

        def start_analysis(e):
            btn_start.disabled = True
            progress_load.visible = True
            text_load.visible = True
            page.update()

            try:
                if global_df[0].endswith('.csv'):
                    df = pd.read_csv(global_df[0])
                else:
                    df = pd.read_excel(global_df[0])

                progress_load.value = 1.0 
                text_load.value = "Daten erfolgreich geladen! ✅"
                progress_analyze.visible = True
                text_analyze.visible = True
                page.update()

                # Zu Seite 2 wechseln (Übergibt den DataFrame)
                build_dashboard(df)

            except Exception as ex:
                status_text.value = f"Fehler beim Laden: {str(ex)}"
                status_text.color = ft.colors.RED
                progress_load.visible = False
                text_load.visible = False
                page.update()

        btn_pick = ft.ElevatedButton(
            "Datei suchen", 
            icon=ft.icons.FOLDER_OPEN, 
            on_click=lambda _: file_picker.pick_files(allowed_extensions=["xlsx", "csv"])
        )
        
        btn_start = ft.FilledButton(
            "Analyse Starten", 
            icon=ft.icons.PLAY_ARROW, 
            disabled=True, 
            on_click=start_analysis,
            style=ft.ButtonStyle(bgcolor=ft.colors.GREEN)
        )

        start_view = ft.Container(
            alignment=ft.alignment.center,
            margin=ft.margin.only(top=100),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Icon(ft.icons.ANALYTICS, size=80, color=ft.colors.BLUE),
                    title,
                    btn_pick,
                    status_text,
                    ft.Divider(height=40, color=ft.colors.TRANSPARENT),
                    btn_start,
                    ft.Column([text_load, progress_load], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    ft.Column([text_analyze, progress_analyze], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ]
            )
        )
        page.add(start_view)
        page.update()

    show_page_1()

ft.app(target=main)