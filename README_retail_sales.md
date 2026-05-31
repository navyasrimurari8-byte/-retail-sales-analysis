# 🛍️ Retail Sales Analysis — End-to-End Data Analytics Project

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.0-green?logo=pandas)
![Seaborn](https://img.shields.io/badge/Seaborn-Visualization-orange)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

---

## 📌 Project Overview

An end-to-end data analysis project on an Indian e-commerce retail dataset containing **31,000+ transaction records**. This project covers the full data analytics workflow — from raw data ingestion and cleaning, through exploratory analysis, to actionable business insights and professional visualisations.

**Business Question:** *Which channels, products, customer segments, and geographies are driving revenue — and where should the business focus to grow?*

---

## 📊 Dataset

| Attribute | Detail |
|---|---|
| Source | Indian E-Commerce Retail Store |
| Records | 31,000+ orders |
| Time Period | Full calendar year |
| Columns | 21 (Order ID, Customer, Gender, Age, Channel, Category, Amount, State, Status, B2B flag, etc.) |

---

## 🔧 Tools & Libraries

| Tool | Purpose |
|---|---|
| Python 3.10+ | Core language |
| Pandas | Data loading, cleaning, transformation |
| NumPy | Numerical operations |
| Matplotlib | Custom chart creation |
| Seaborn | Statistical visualisations |
| OpenPyXL | Excel file reading |

---

## 📁 Project Structure

```
retail-sales-analysis/
│
├── retail_sales_analysis.py     # Main analysis script
├── store_data.xlsx              # Raw dataset
│
├── charts/
│   ├── chart1_monthly_revenue.png
│   ├── chart2_channel_analysis.png
│   ├── chart3_demographics.png
│   ├── chart4_product_analysis.png
│   ├── chart5_geographic.png
│   ├── chart6_fulfilment.png
│   └── chart7_correlation.png
│
└── README.md
```

---

## 🚀 How to Run

```bash
# 1. Clone the repository
git clone https://github.com/navyasrimurari/retail-sales-analysis.git
cd retail-sales-analysis

# 2. Install dependencies
pip install pandas numpy matplotlib seaborn openpyxl

# 3. Run the analysis
python retail_sales_analysis.py
```

---

## 🔍 Analysis Steps

### Step 1 — Data Loading
- Loaded 31,000+ rows from Excel using Pandas + OpenPyXL
- Inspected schema, data types, and shape

### Step 2 — Data Cleaning
- Renamed inconsistent column headers
- Handled missing values using median imputation
- Removed duplicate records
- Parsed date columns and extracted Month/Year features
- Standardised text columns (Title Case formatting)
- Validated and corrected numeric columns (Amount, Qty)

### Step 3 — KPI Computation
Key metrics surfaced:

| KPI | Value |
|---|---|
| Total Revenue | ₹21.2M+ |
| Total Orders | 28,000+ |
| Average Order Value | ~₹760 |
| Unique Customers | 28,000+ |
| Delivery Success Rate | 83%+ |

### Step 4 — Exploratory Data Analysis
- Monthly revenue trend analysis
- Sales channel performance comparison
- Customer demographic breakdown (gender, age group)
- Product category revenue ranking
- Geographic revenue by state (Top 10)
- Order status and fulfilment analysis
- B2B vs B2C revenue split
- Correlation matrix for numeric features

### Step 5 — Visualisations (7 Charts)
- Monthly revenue bar + line combo chart
- Horizontal bar chart — channel revenue
- Pie chart — gender distribution
- Grouped bar — age group revenue
- Top 10 states horizontal bar
- Order status pie chart
- Correlation heatmap

---

## 💡 Key Business Insights

1. **Amazon is the #1 revenue channel** — contributing the largest share of total sales. Myntra and Flipkart follow. Marketing budgets should prioritise these platforms.

2. **Women drive ~65% of revenue** — product assortment and ad targeting should be women-first across all channels.

3. **Adult age group (26–45) is the highest-value segment** — loyalty programmes and upsell campaigns should focus here.

4. **Sets and Kurtas are the top-performing categories** — inventory planning should ensure these are never out of stock during peak months.

5. **Maharashtra, Karnataka, and Uttar Pradesh** lead in revenue — geographic expansion into Tier-2 cities in these states could yield strong returns.

6. **83%+ delivery success rate** is strong, but the cancellation rate signals a need to review fulfilment SLAs with certain logistics partners.

7. **B2B segment is small but strategic** — targeted B2B outreach could unlock higher-margin, bulk-order revenue.

---

## 📈 Visualisation Preview

| Chart | Insight |
|---|---|
| Monthly Revenue | Identifies peak and low-demand months for inventory planning |
| Channel Analysis | Reveals which platforms drive most orders and revenue |
| Demographics | Shows gender and age-based purchasing patterns |
| Product Analysis | Highlights best and worst performing categories |
| Geographic | Maps revenue concentration by state |
| Fulfilment | Tracks delivery vs cancellation rates |
| Correlation | Identifies relationships between numeric variables |

---

## 👩‍💻 About the Author

**Navya Sri Murari** — Data Analyst | Power BI Developer | Python | SQL | Tableau

📧 navyasrimurari8@gmail.com
🔗 [Tableau Public Portfolio](https://public.tableau.com/app/profile/navya.murari/vizzes)
📍 Hyderabad, India | Open to Remote

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
