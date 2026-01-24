"""
Sales Method Comparison Analysis
=================================

Business Question:
How many customers were there for each approach?

This analysis examines the customer distribution across the three sales methods
tested during the 6-week experiment: Email, Call, and Email + Call.

Related README Section:
https://github.com/Isaaccev7/sales-strategy-experiment-analysis#1-customer-distribution-by-sales-method

Author: Isaac
Last Updated: January 2026
"""

# ============================================================================
# 1. IMPORTS AND CONFIGURATION
# ============================================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Visualization configuration
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Define consistent color mapping for all visualizations
COLOR_MAP = {
    'Email': '#3b82f6',        # Blue - Mass reach method
    'Call': '#10b981',         # Green - High-touch method
    'Email + Call': '#8b5cf6'  # Purple - Hybrid method
}

# ============================================================================
# 2. DATA LOADING
# ============================================================================

# Load cleaned data
product_sales = pd.read_csv("../data/raw/product_sales.csv")

# Apply data cleaning (same as 01_data_cleaning.py)
product_sales["sales_method"] = product_sales["sales_method"].replace({
    "em + call": "Email + Call",
    "email": "Email"
})
product_sales.dropna(subset=['revenue'], inplace=True)

print("="*80)
print("DATA LOADED SUCCESSFULLY")
print("="*80)
print(f"Total records: {len(product_sales):,}")
print(f"Date range: Week {product_sales['week'].min()} to Week {product_sales['week'].max()}")
print(f"Sales methods: {', '.join(product_sales['sales_method'].unique())}")

# ============================================================================
# 3. CUSTOMER DISTRIBUTION ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("CUSTOMER DISTRIBUTION BY SALES METHOD")
print("="*80)

# Calculate unique customers per method
customers_per_method = (
    product_sales
    .groupby("sales_method")["customer_id"]
    .nunique()
    .sort_values(ascending=False)
)

# Order methods according to color map for consistency
customers_per_method = customers_per_method.reindex(COLOR_MAP.keys())

# Display results
print("\nNumber of unique customers by method:")
print("-" * 40)
for method, count in customers_per_method.items():
    percentage = (count / product_sales['customer_id'].nunique()) * 100
    print(f"{method:15} {count:6,} customers ({percentage:5.1f}%)")

print("-" * 40)
print(f"{'TOTAL':15} {product_sales['customer_id'].nunique():6,} customers (100.0%)")

# ============================================================================
# 4. STATISTICAL SUMMARY
# ============================================================================

print("\n" + "="*80)
print("RESOURCE ALLOCATION ANALYSIS")
print("="*80)

print("\nCustomer allocation strategy:")
total_customers = product_sales['customer_id'].nunique()

for method in COLOR_MAP.keys():
    count = customers_per_method[method]
    pct = (count / total_customers) * 100
    
    # Interpret allocation strategy
    if pct >= 45:
        strategy = "High-volume scalability bet"
    elif pct >= 30:
        strategy = "Significant investment"
    else:
        strategy = "Limited allocation/pilot test"
    
    print(f"  {method:15} {pct:5.1f}% → {strategy}")

# ============================================================================
# 5. VISUALIZATION: CUSTOMERS BY METHOD
# ============================================================================

print("\n" + "="*80)
print("GENERATING VISUALIZATION")
print("="*80)

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))

# Create bar chart
bars = customers_per_method.plot(
    kind='bar',
    ax=ax,
    color=[COLOR_MAP[method] for method in customers_per_method.index],
    edgecolor='black',
    linewidth=1.2,
    alpha=0.8
)

# Styling
ax.set_title(
    'Number of Customers by Sales Method',
    fontsize=16,
    fontweight='bold',
    pad=20
)
ax.set_xlabel('Sales Method', fontsize=12, fontweight='bold')
ax.set_ylabel('Number of Customers', fontsize=12, fontweight='bold')
ax.set_xticklabels(customers_per_method.index, rotation=45, ha='right')
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Add value labels on bars
for i, (method, count) in enumerate(customers_per_method.items()):
    percentage = (count / total_customers) * 100
    
    # Main count label
    ax.text(
        i, count + max(customers_per_method.values) * 0.01,
        f'{count:,}',
        ha='center', va='bottom',
        fontsize=11, fontweight='bold'
    )
    
    # Percentage label
    ax.text(
        i, count / 2,
        f'{percentage:.1f}%',
        ha='center', va='center',
        fontsize=10, fontweight='bold',
        color='white'
    )

# Format y-axis with comma separator
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))

plt.tight_layout()

# Save figure
output_path = '../visualizations/1_customers_by_method.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✓ Visualization saved: {output_path}")

plt.show()

# ============================================================================
# 6. KEY INSIGHTS
# ============================================================================

print("\n" + "="*80)
print("KEY INSIGHTS")
print("="*80)

print("""
Customer Allocation Summary:
---------------------------
1. Email received the highest allocation (50%) - consistent with a 
   scalability-focused strategy requiring minimal team effort

2. Call received significant investment (34%) despite requiring 30 minutes
   per customer - indicating initial hypothesis about high-touch value

3. Email + Call received smallest allocation (16%) - treated as complex
   pilot method requiring both email setup and call time

Critical Question:
-----------------
Did this 50/34/16 resource allocation match actual performance outcomes?
→ See revenue analysis in subsequent notebooks to evaluate ROI by method

Next Analysis:
-------------
- 03_revenue_distribution.py: Does customer volume correlate with revenue?
- 04_temporal_trends.py: Did allocation strategy prove sustainable?
- 05_efficiency_analysis.py: Revenue per minute validates resource allocation
""")

print("="*80)
print("ANALYSIS COMPLETE")
print("="*80)

# ============================================================================
# TECHNICAL NOTES
# ============================================================================
"""
Analysis Methodology:
--------------------
- Metric: Unique customer count per sales_method
- Calculation: groupby('sales_method').nunique()
- Time period: 6-week experiment (all weeks included)
- Data quality: No duplicate customer_ids, complete data

Visualization Design:
--------------------
- Chart type: Vertical bar chart (clear comparison)
- Color coding: Consistent across all project visualizations
  * Blue (Email): High volume, low touch
  * Green (Call): Medium volume, high touch  
  * Purple (Email + Call): Low volume, hybrid approach
- Labels: Absolute counts + percentages for context

Business Context:
----------------
This distribution reflects initial resource allocation decisions made
before knowing performance outcomes. The key question is whether this
allocation aligned with actual revenue generation efficiency.

Results should be interpreted alongside:
- Revenue per customer (are we focusing on the right segments?)
- Revenue per minute (is our time investment optimized?)
- Revenue trends over time (is our strategy sustainable?)
"""