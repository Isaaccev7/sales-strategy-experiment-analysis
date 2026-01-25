"""
Revenue Distribution Analysis
==============================

Business Question:
What does the spread of the revenue look like overall? And for each method?

This analysis examines how revenue is distributed across the three sales methods,
revealing distinct customer value patterns for Email, Call, and Email + Call.

Related README Section:
https://github.com/Isaaccev7/sales-strategy-experiment-analysis#2-revenue-distribution-analysis

Author: Isaac
Last Updated: November 2025
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

# Define consistent color mapping (same as previous notebooks)
COLOR_MAP = {
    'Email': '#3b82f6',        # Blue - Mass reach method
    'Call': '#10b981',         # Green - High-touch method
    'Email + Call': '#8b5cf6'  # Purple - Hybrid method
}

# ============================================================================
# 2. DATA LOADING
# ============================================================================

# Load cleaned data (processed by 01_data_cleaning.py)
product_sales = pd.read_csv("../data/processed/product_sales_clean.csv")

print("="*80)
print("DATA LOADED SUCCESSFULLY")
print("="*80)
print(f"Total transactions: {len(product_sales):,}")
print("✓ Using pre-cleaned dataset from 01_data_cleaning.py")
print(f"Total revenue: ${product_sales['revenue'].sum():,.2f}")
print(f"Overall mean revenue: ${product_sales['revenue'].mean():.2f}")

# ============================================================================
# 3. OVERALL REVENUE DISTRIBUTION ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("OVERALL REVENUE DISTRIBUTION")
print("="*80)

# Calculate key statistics
overall_stats = {
    'Mean': product_sales['revenue'].mean(),
    'Median': product_sales['revenue'].median(),
    'Std Dev': product_sales['revenue'].std(),
    'Min': product_sales['revenue'].min(),
    'Max': product_sales['revenue'].max(),
    'Q1 (25%)': product_sales['revenue'].quantile(0.25),
    'Q3 (75%)': product_sales['revenue'].quantile(0.75)
}

print("\nOverall Revenue Statistics:")
print("-" * 40)
for stat, value in overall_stats.items():
    print(f"{stat:12} ${value:>10.2f}")

IQR = overall_stats['Q3 (75%)'] - overall_stats['Q1 (25%)']
print(f"{'IQR':12} ${IQR:>10.2f}")

# ============================================================================
# 4. REVENUE DISTRIBUTION BY SALES METHOD
# ============================================================================

print("\n" + "="*80)
print("REVENUE DISTRIBUTION BY SALES METHOD")
print("="*80)

methods = list(COLOR_MAP.keys())

# Calculate statistics for each method
method_stats = {}
for method in methods:
    method_data = product_sales[product_sales['sales_method'] == method]['revenue']
    method_stats[method] = {
        'count': len(method_data),
        'mean': method_data.mean(),
        'median': method_data.median(),
        'std': method_data.std(),
        'min': method_data.min(),
        'max': method_data.max(),
        'Q1': method_data.quantile(0.25),
        'Q3': method_data.quantile(0.75)
    }

# Display detailed statistics
for method in methods:
    stats = method_stats[method]
    IQR = stats['Q3'] - stats['Q1']
    customer_share = (stats['count'] / len(product_sales)) * 100
    
    print(f"\n{method}:")
    print("-" * 40)
    print(f"  Customers:    {stats['count']:>6,} ({customer_share:>5.1f}% of total)")
    print(f"  Mean:         ${stats['mean']:>9.2f}")
    print(f"  Median:       ${stats['median']:>9.2f}")
    print(f"  Std Dev:      ${stats['std']:>9.2f}")
    print(f"  Range:        ${stats['min']:>9.2f} - ${stats['max']:.2f}")
    print(f"  IQR:          ${IQR:>9.2f} (Q1: ${stats['Q1']:.2f}, Q3: ${stats['Q3']:.2f})")

# ============================================================================
# 5. COMPARATIVE PERFORMANCE ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("COMPARATIVE PERFORMANCE ANALYSIS")
print("="*80)

overall_mean = product_sales['revenue'].mean()

print(f"\nOverall benchmark: ${overall_mean:.2f}")
print("-" * 40)

for method in methods:
    method_mean = method_stats[method]['mean']
    performance_vs_overall = ((method_mean - overall_mean) / overall_mean) * 100
    
    # Determine performance indicator
    if performance_vs_overall > 20:
        indicator = "🚀 Strong outperformer"
    elif performance_vs_overall > 0:
        indicator = "✓ Above average"
    elif performance_vs_overall > -20:
        indicator = "⚠ Below average"
    else:
        indicator = "❌ Significant underperformer"
    
    print(f"\n{method}:")
    print(f"  Mean revenue:        ${method_mean:>9.2f}")
    print(f"  vs Overall:          {performance_vs_overall:>+8.1f}%")
    print(f"  Performance:         {indicator}")

# Identify best and worst performers
best_method = max(methods, key=lambda x: method_stats[x]['mean'])
worst_method = min(methods, key=lambda x: method_stats[x]['mean'])

print("\n" + "="*80)
print(f"🏆 Best performer:  {best_method} (${method_stats[best_method]['mean']:.2f})")
print(f"❌ Worst performer: {worst_method} (${method_stats[worst_method]['mean']:.2f})")
print(f"   Performance gap: {(method_stats[best_method]['mean'] / method_stats[worst_method]['mean'] - 1) * 100:.1f}%")
print("="*80)

# ============================================================================
# 6. VISUALIZATION: REVENUE DISTRIBUTION HISTOGRAMS
# ============================================================================

print("\n" + "="*80)
print("GENERATING VISUALIZATION: HISTOGRAMS")
print("="*80)

fig, ax = plt.subplots(figsize=(12, 7))

# Create overlaid histograms
for method in methods:
    method_data = product_sales[product_sales['sales_method'] == method]['revenue']
    ax.hist(
        method_data,
        bins=20,
        alpha=0.6,
        color=COLOR_MAP[method],
        edgecolor='black',
        linewidth=0.5,
        label=f'{method} (n={len(method_data):,})'
    )

# Styling
ax.set_title('Revenue Distribution by Sales Method', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Revenue ($)', fontsize=12, fontweight='bold')
ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
ax.legend(loc='upper right', fontsize=10)
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Format x-axis with dollar signs
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${int(x)}'))

plt.tight_layout()

# Save figure
output_path = '../visualizations/2D_revenue_by_method_histograms.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✓ Histogram saved: {output_path}")

plt.show()

# ============================================================================
# 7. VISUALIZATION: REVENUE DISTRIBUTION BOXPLOTS
# ============================================================================

print("\n" + "="*80)
print("GENERATING VISUALIZATION: BOXPLOTS")
print("="*80)

fig, ax = plt.subplots(figsize=(10, 6))

# Create boxplots for each method
positions = range(len(methods))
boxplot_data = []

for i, method in enumerate(methods):
    method_data = product_sales[product_sales['sales_method'] == method]['revenue']
    boxplot_data.append(method_data)
    
    # Create boxplot
    bp = ax.boxplot(
        method_data,
        positions=[i],
        widths=0.6,
        patch_artist=True,
        boxprops=dict(facecolor=COLOR_MAP[method], alpha=0.7, edgecolor='black', linewidth=1.2),
        medianprops=dict(color='yellow', linewidth=2.5),
        whiskerprops=dict(linewidth=1.5, color='black'),
        capprops=dict(linewidth=1.5, color='black'),
        flierprops=dict(marker='o', markersize=4, alpha=0.5, markerfacecolor=COLOR_MAP[method])
    )
    
    # Add mean marker
    mean_val = method_data.mean()
    ax.plot(i, mean_val, marker='D', markersize=8, color='red', 
            markeredgecolor='darkred', markeredgewidth=1.5, label='Mean' if i == 0 else '')

# Styling
ax.set_title('Revenue Distribution by Sales Method', fontsize=16, fontweight='bold', pad=20)
ax.set_ylabel('Revenue ($)', fontsize=12, fontweight='bold')
ax.set_xlabel('Sales Method', fontsize=12, fontweight='bold')
ax.set_xticks(positions)
ax.set_xticklabels(methods, rotation=45, ha='right')
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.legend(loc='upper left', fontsize=10)

# Format y-axis with dollar signs
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${int(x)}'))

plt.tight_layout()

# Save figure
output_path = '../visualizations/2C_revenue_by_method_boxplots.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✓ Boxplot saved: {output_path}")

plt.show()

# ============================================================================
# 8. KEY INSIGHTS
# ============================================================================

print("\n" + "="*80)
print("KEY INSIGHTS")
print("="*80)

print("""
Revenue Distribution Findings:
-----------------------------
1. Three Distinct Revenue Patterns:
   - Call: Clustered at $40-50 (resistance, minimal purchases)
   - Email: Centered at $90-100 (standard purchases)
   - Email + Call: Dominates $150-220+ (premium purchases)

2. No Overlap Between Methods:
   - Email + Call minimum ($122) > Email maximum ($149)
   - These aren't variations—they're fundamentally different behaviors

3. Performance Gap:
   - Email + Call generates 286% more revenue than Call
   - Email + Call generates 89% more revenue than Email
   
4. Statistical Significance:
   - Low standard deviation in Call (consistent low value)
   - Moderate spread in Email (standard product adoption)
   - Higher variance in Email + Call (premium tier with range)

Business Implications:
---------------------
- Call generates RESISTANCE (customers buy minimum to end interaction)
- Email generates INTEREST (customers make informed standard purchases)
- Email + Call generates TRUST (warm conversation unlocks premium buying)

The email pre-warms the customer, transforming them from skeptical to receptive.
A 10-minute conversation with an informed buyer beats 30 minutes of cold calling.

Next Analysis:
-------------
- 04_temporal_trends.py: Are these patterns sustainable over time?
- 05_efficiency_analysis.py: What's the revenue per minute invested?
""")

print("="*80)
print("ANALYSIS COMPLETE")
print("="*80)

# ============================================================================
# TECHNICAL NOTES
# ============================================================================
"""
Statistical Methods:
-------------------
- Descriptive statistics: mean, median, std dev, quartiles
- Comparative analysis: performance vs overall benchmark
- Distribution visualization: histograms (shape) + boxplots (statistics)

Visualization Choices:
---------------------
1. Histograms (overlaid):
   - Shows distribution shape and frequency
   - Reveals non-overlapping revenue ranges
   - Alpha transparency allows pattern comparison

2. Boxplots:
   - Shows median, quartiles, range, outliers
   - Easy comparison of central tendency
   - Yellow median line + red diamond mean marker
   - Outliers show revenue ceiling for each method

Key Statistical Findings:
------------------------
- Email + Call IQR ($156-191) is entirely above Email max ($149)
- Call has narrowest IQR (consistent low performance)
- Email + Call has highest mean AND median (not skewed by outliers)

Business Context:
----------------
Revenue distribution reveals that sales methods don't just differ in 
efficiency—they activate fundamentally different customer behaviors:

Call → Defensive buying (minimal purchase to end interaction)
Email → Informed buying (standard product adoption)
Email + Call → Consultative buying (trust-based premium purchases)

This explains why Email + Call outperforms despite lower volume.
Quality of customer engagement matters more than quantity of contacts.
"""