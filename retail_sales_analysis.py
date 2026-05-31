import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

#Plot styling
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    'figure.dpi': 130,
    'axes.titlesize': 13,
    'axes.titleweight': 'bold',
    'axes.labelsize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'figure.facecolor': '#FAFAFA',
})

print("=" * 60)
print("  RETAIL SALES ANALYSIS — Navya Sri Murari")
print("=" * 60)

# load data
print("\n[1/6] Loading data...")
df = pd.read_excel("store_data.xlsx", engine='openpyxl')
print(f"  Loaded  : {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f"  Columns : {list(df.columns)}")
# Data cleaning
print("\n[2/6] Cleaning data...")

# Rename for convenience
df.rename(columns={
    'Channel ': 'Channel',
    'ship-city': 'City',
    'ship-state': 'State',
    'ship-postal-code': 'Postal Code',
    'ship-country': 'Country'
}, inplace=True)

# Check missing values
missing = df.isnull().sum()
missing = missing[missing > 0]
if len(missing) > 0:
    print(f"  Missing values found:\n{missing}")
else:
    print("  No missing values found.")

# Remove duplicates
before = len(df)
df.drop_duplicates(inplace=True)
print(f"  Duplicates removed: {before - len(df)}")

# Parse date column
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Month_Num'] = df['Date'].dt.month
df['Month_Name'] = df['Date'].dt.strftime('%b')

# Fix Amount column (ensure numeric)
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
df['Amount'].fillna(df['Amount'].median(), inplace=True)

# Fix Qty column
df['Qty'] = pd.to_numeric(df['Qty'], errors='coerce')
df['Qty'].fillna(1, inplace=True)

# Standardise text columns
for col in ['Gender', 'Age Group', 'Status', 'Channel', 'Category', 'Size']:
    df[col] = df[col].astype(str).str.strip().str.title()

print(f"  Final clean dataset: {df.shape[0]:,} rows")


# KPI
print("\n[3/6] Computing KPIs...")

total_revenue    = df['Amount'].sum()
total_orders     = df['Order ID'].nunique()
avg_order_value  = total_revenue / total_orders
total_qty        = df['Qty'].sum()
unique_customers = df['Cust ID'].nunique()
delivery_rate    = (df['Status'] == 'Delivered').mean() * 100
cancellation_rate= (df['Status'] == 'Cancelled').mean() * 100

print("\n" + "=" * 45)
print("  KEY PERFORMANCE INDICATORS")
print("=" * 45)
print(f"  Total Revenue         : ₹{total_revenue:,.0f}")
print(f"  Total Orders          : {total_orders:,}")
print(f"  Average Order Value   : ₹{avg_order_value:,.2f}")
print(f"  Total Units Sold      : {total_qty:,.0f}")
print(f"  Unique Customers      : {unique_customers:,}")
print(f"  Delivery Rate         : {delivery_rate:.1f}%")
print(f"  Cancellation Rate     : {cancellation_rate:.1f}%")
print("=" * 45)


# Analysis
print("\n[4/6] Running exploratory analysis...")

# Monthly revenue trend
monthly = df.groupby(['Month_Num', 'Month_Name'])['Amount'].sum().reset_index()
monthly = monthly.sort_values('Month_Num')

# Sales by channel
channel_rev = df.groupby('Channel')['Amount'].sum().sort_values(ascending=False)

# Sales by category
category_rev = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)

# Gender distribution
gender_counts = df['Gender'].value_counts()
gender_revenue = df.groupby('Gender')['Amount'].sum()

# Age group analysis
age_rev = df.groupby('Age Group')['Amount'].sum().sort_values(ascending=False)

# Top 10 states
state_rev = df.groupby('State')['Amount'].sum().sort_values(ascending=False).head(10)

# Order status breakdown
status_counts = df['Status'].value_counts()

# B2B vs B2C
b2b_rev = df.groupby('B2B')['Amount'].sum()

print("  Analysis complete.")

# Visuals
print("\n[5/6] Generating visualisations...")

COLORS = ['#2E75B6','#4BACC6','#70AD47','#ED7D31','#FFC000','#A5A5A5','#5A5A8F','#C55A11']

# ── Chart 1 : Monthly Revenue Trend
fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(monthly['Month_Name'], monthly['Amount'] / 1e6,
       color=COLORS[0], alpha=0.7, label='Revenue (₹M)')
ax2 = ax.twinx()
ax2.plot(monthly['Month_Name'], monthly['Amount'] / 1e6,
         color=COLORS[2], marker='o', linewidth=2.5, markersize=7, label='Trend')
ax.set_title('Monthly Revenue Trend', pad=12)
ax.set_xlabel('Month')
ax.set_ylabel('Revenue (₹ Millions)')
ax2.set_ylabel('Revenue (₹ Millions)')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₹{x:.1f}M'))
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₹{x:.1f}M'))
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
plt.tight_layout()
plt.savefig('chart1_monthly_revenue.png', bbox_inches='tight')
plt.show()
print("  Saved: chart1_monthly_revenue.png")

# ── Chart 2 : Sales Channel Performance ─────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
# Revenue by channel
axes[0].barh(channel_rev.index, channel_rev.values / 1e6,
             color=COLORS[:len(channel_rev)])
axes[0].set_title('Revenue by Sales Channel')
axes[0].set_xlabel('Revenue (₹ Millions)')
axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₹{x:.1f}M'))
for i, v in enumerate(channel_rev.values):
    axes[0].text(v / 1e6 + 0.05, i, f'₹{v/1e6:.1f}M', va='center', fontsize=9)

# Order count by channel
channel_orders = df.groupby('Channel')['Order ID'].nunique().sort_values(ascending=False)
axes[1].bar(channel_orders.index, channel_orders.values,
            color=COLORS[:len(channel_orders)])
axes[1].set_title('Number of Orders by Channel')
axes[1].set_ylabel('Order Count')
axes[1].tick_params(axis='x', rotation=30)
for i, v in enumerate(channel_orders.values):
    axes[1].text(i, v + 30, f'{v:,}', ha='center', fontsize=9)

plt.suptitle('Sales Channel Analysis', fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('chart2_channel_analysis.png', bbox_inches='tight')
plt.show()
print("  Saved: chart2_channel_analysis.png")

# ── Chart 3 : Customer Demographics
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Gender pie
axes[0].pie(gender_counts.values, labels=gender_counts.index,
            autopct='%1.1f%%', colors=['#2E75B6','#ED7D31'],
            startangle=90, wedgeprops={'edgecolor':'white','linewidth':2})
axes[0].set_title('Orders by Gender')

# Age group revenue
axes[1].bar(age_rev.index, age_rev.values / 1e6,
            color=COLORS[:len(age_rev)])
axes[1].set_title('Revenue by Age Group')
axes[1].set_ylabel('Revenue (₹ Millions)')
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₹{x:.0f}M'))
axes[1].tick_params(axis='x', rotation=20)

# Gender revenue comparison
axes[2].bar(gender_revenue.index, gender_revenue.values / 1e6,
            color=['#2E75B6','#ED7D31'], width=0.5)
axes[2].set_title('Revenue by Gender')
axes[2].set_ylabel('Revenue (₹ Millions)')
axes[2].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₹{x:.0f}M'))
for i, v in enumerate(gender_revenue.values):
    axes[2].text(i, v / 1e6 + 0.3, f'₹{v/1e6:.1f}M', ha='center', fontsize=10, fontweight='bold')

plt.suptitle('Customer Demographics Analysis', fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('chart3_demographics.png', bbox_inches='tight')
plt.show()
print("  Saved: chart3_demographics.png")

# ── Chart 4 : Product Category Analysis
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

axes[0].barh(category_rev.index, category_rev.values / 1e6,
             color=COLORS[:len(category_rev)])
axes[0].set_title('Revenue by Product Category')
axes[0].set_xlabel('Revenue (₹ Millions)')
axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₹{x:.0f}M'))
for i, v in enumerate(category_rev.values):
    axes[0].text(v / 1e6 + 0.1, i, f'₹{v/1e6:.1f}M', va='center', fontsize=9)

# Size distribution
size_counts = df['Size'].value_counts()
axes[1].bar(size_counts.index, size_counts.values, color=COLORS[:len(size_counts)])
axes[1].set_title('Orders by Size')
axes[1].set_ylabel('Number of Orders')
axes[1].tick_params(axis='x', rotation=15)
for i, v in enumerate(size_counts.values):
    axes[1].text(i, v + 50, f'{v:,}', ha='center', fontsize=8)

plt.suptitle('Product Analysis', fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('chart4_product_analysis.png', bbox_inches='tight')
plt.show()
print("  Saved: chart4_product_analysis.png")

#Chart 5 : Geographic Analysis
fig, ax = plt.subplots(figsize=(12, 5))
bars = ax.barh(state_rev.index[::-1], state_rev.values[::-1] / 1e6,
               color=COLORS[0])
ax.set_title('Top 10 States by Revenue', pad=12)
ax.set_xlabel('Revenue (₹ Millions)')
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₹{x:.0f}M'))
for bar, v in zip(bars, state_rev.values[::-1]):
    ax.text(v / 1e6 + 0.1, bar.get_y() + bar.get_height()/2,
            f'₹{v/1e6:.1f}M', va='center', fontsize=9)
plt.tight_layout()
plt.savefig('chart5_geographic.png', bbox_inches='tight')
plt.show()
print("  Saved: chart5_geographic.png")

#Chart 6 : Order Status & Fulfilment
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

colors_status = ['#70AD47','#FF0000','#FFC000','#2E75B6','#A5A5A5','#ED7D31']
axes[0].pie(status_counts.values, labels=status_counts.index,
            autopct='%1.1f%%', colors=colors_status[:len(status_counts)],
            startangle=140, wedgeprops={'edgecolor':'white','linewidth':2})
axes[0].set_title('Order Status Breakdown')

# B2B vs B2C
b2b_labels = ['B2C (Regular)', 'B2B (Business)']
axes[1].pie(b2b_rev.values, labels=b2b_labels,
            autopct='%1.1f%%', colors=['#2E75B6','#ED7D31'],
            startangle=90, wedgeprops={'edgecolor':'white','linewidth':2})
axes[1].set_title('B2B vs B2C Revenue Split')

plt.suptitle('Order Fulfilment Analysis', fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('chart6_fulfilment.png', bbox_inches='tight')
plt.show()
print("  Saved: chart6_fulfilment.png")

# Chart 7 : Correlation Heatmap
fig, ax = plt.subplots(figsize=(7, 5))
num_cols = df[['Amount', 'Qty', 'Age', 'Month_Num']].copy()
corr = num_cols.corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='Blues',
            linewidths=0.5, ax=ax, square=True,
            cbar_kws={'shrink': 0.8})
ax.set_title('Correlation Matrix — Numeric Features', pad=12)
plt.tight_layout()
plt.savefig('chart7_correlation.png', bbox_inches='tight')
plt.show()
print("  Saved: chart7_correlation.png")

# Insights summary
print("\n[6/6] Business Insights Summary")
print("\n" + "=" * 55)
print("  ACTIONABLE BUSINESS INSIGHTS")
print("=" * 55)

top_channel = channel_rev.index[0]
top_channel_pct = channel_rev.iloc[0] / channel_rev.sum() * 100
top_category = category_rev.index[0]
top_state = state_rev.index[0]
top_age = age_rev.index[0]

print(f"""
  REVENUE & ORDERS
  ─────────────────────────────────────────────────────
  • Total revenue of ₹{total_revenue/1e6:.1f}M generated from
    {total_orders:,} orders across {unique_customers:,} customers.
  • Average order value: ₹{avg_order_value:,.0f}

  CHANNEL STRATEGY
  ─────────────────────────────────────────────────────
  • {top_channel} is the #1 revenue channel ({top_channel_pct:.1f}% of sales).
  • Amazon and Myntra together account for majority of
    online sales — these should be priority channels.

  PRODUCT & CATEGORY
  ─────────────────────────────────────────────────────
  • '{top_category}' is the best-performing category.
  • M and L sizes dominate order volume — inventory
    planning should prioritise these sizes.

  CUSTOMER INSIGHTS
  ─────────────────────────────────────────────────────
  • Women drive significantly higher revenue than men —
    marketing campaigns should be women-first.
  • '{top_age}' age group is the highest-value segment.

  GEOGRAPHY
  ─────────────────────────────────────────────────────
  • {top_state} leads all states in revenue.
  • Top 3 states contribute disproportionately —
    regional expansion opportunity exists.

  OPERATIONS
  ─────────────────────────────────────────────────────
  • {delivery_rate:.1f}% delivery success rate — strong fulfilment.
  • {cancellation_rate:.1f}% cancellation rate — monitor for trends.
  • B2B segment, while smaller, may offer higher-margin
    growth opportunity.
""")
print("=" * 55)
print("  Analysis complete! All charts saved as PNG files.")
print("=" * 55)
