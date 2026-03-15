# FlowPOS Insight 📊

### *Turning Cash Register Data into Actionable Business Intelligence*

**FlowPOS Insight** is a Python-based data analysis tool designed to process raw export data from Point-of-Sale (POS) systems. By transforming messy CSV/Excel exports into visual dashboards, it helps business owners understand sales trends, customer behavior, and product correlations.

> [!NOTE]
> **Status:** This project is currently a **Draft/Work-in-Progress**. Features are being added step-by-step to improve data cleaning and advanced predictive insights.

---

## 🚀 Features

The current version of the script performs several key analyses:

* **Sales Trends:** Daily and monthly revenue tracking to identify growth or seasonal dips.
* **Peak Time Analysis:** A heatmap of "Weekday vs. Hour" to optimize staff scheduling.
* **Product Performance:** Identification of Top 10 bestsellers and their hourly sales distribution.
* **Market Basket Analysis:** Discovering which products are frequently bought together (Top Combinations).
* **Risk & Volatility:** Boxplot analysis to see how much daily revenue fluctuates per weekday.
* **Transaction Insights:** Average basket value (receipt totals) and payment method distribution (Cash vs. Card).
* **Tax & Location Analysis:** Comparison between In-House (19%) and Take-Away (7%) sales.

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Data Handling:** `pandas`
* **Visualization:** `matplotlib`, `seaborn`
* **Math & Logic:** `itertools`, `collections`

---

## 📂 Installation & Setup

1. **Clone the repository:**
```bash
git clone https://github.com/diyaino/flowpos-insight.git
cd flowpos-insight

```


2. **Install dependencies:**
```bash
pip install pandas matplotlib seaborn openpyxl

```


3. **Prepare your data:**
* Place your POS export file (Excel/CSV) in the project directory.
* Update the `file_path` variable in the script to point to your data.



---

## 📊 Sample Visualizations

The script generates several high-quality plots, including:

1. **Revenue Heatmaps:** Identifying the "Golden Hours" of your business.
2. **Monthly Highlights:** Automatically suggesting the best "Combo Offer" for each month based on historical pairings.
3. **Payment Split:** A breakdown of how customers prefer to pay.

---

## 📝 Roadmap / To-Do

* [ ] Implement automated file detection (glob).
* [ ] Add PDF report generation for monthly summaries.
* [ ] Improve LaTeX support for professional font rendering in plots.
* [ ] Develop a Streamlit Dashboard for interactive filtering.
* [ ] Add support for multiple POS export formats.

---

## 🤝 Contributing

Since this is a draft, contributions are more than welcome! Feel free to open an issue or submit a pull request if you have ideas for better data cleaning or new visualization types.

---

## ⚖️ License

Distributed under the MIT License. See `LICENSE` for more information.

---
