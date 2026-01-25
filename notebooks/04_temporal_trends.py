"""
Revenue Trends Over Time Analysis
==================================

Business Question:
Was there any difference in revenue over time for each of the methods?

This analysis examines how revenue evolved across the 6-week experiment period
for each sales method, revealing critical insights about sustainability and
method effectiveness over time.

Related README Section:
https://github.com/Isaaccev7/sales-strategy-experiment-analysis#3-revenue-trends-over-time

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

print(f"Analysis period: Week {product_sales['week'].min()} to Week {product_sales['week'].max()}")
print(f"Total revenue: ${product_sales['revenue'].sum():,.2f}")

# ============================================================================
# 3. TEMPORAL AGGREGATION
# ============================================================================

print("\n" + "="*80)
print("AGGREGATING REVENUE BY WEEK AND METHOD")
print("="*80)

methods = list(COLOR_MAP.keys())

# Calculate total revenue by week and method
revenue_by_week = (
    product_sales
    .groupby(['week', 'sales_method'])['revenue']
    .sum()
    .reset_index()
)

# Create pivot table for easier analysis
revenue_pivot = revenue_by_week.pivot(
    index='week',
    columns='sales_method',
    values='revenue'
)

# Order columns according to color map for consistency
revenue_pivot = revenue_pivot[methods]

print(f"✓ Aggregated {len(revenue_by_week)} data points")
print(f"✓ Weeks analyzed: {revenue_pivot.index.min()} to {revenue_pivot.index.max()}")

# ============================================================================
# 4. WEEKLY REVENUE SUMMARY TABLE
# ============================================================================

print("\n" + "="*80)
print("TOTAL REVENUE BY WEEK AND METHOD")
print("="*80)

# Display formatted table
print("\n{:<8} {:>12} {:>12} {:>15} {:>12}".format('Week', 'Email', 'Call', 'Email + Call', 'Total'))
print("-" * 63)

for week in sorted(revenue_pivot.index):
    week_data = revenue_pivot.loc[week]
    week_total = week_data.sum()
    
    print("{:<8} ${:>11,} ${:>11,} ${:>14,} ${:>11,}".format(
        f"Week {week}",
        int(week_data['Email']),
        int(week_data['Call']),
        int(week_data['Email + Call']),
        int(week_total)
    ))

# Display totals
print("-" * 63)
method_totals = revenue_pivot.sum()
grand_total = method_totals.sum()

print("{:<8} ${:>11,} ${:>11,} ${:>14,} ${:>11,}".format(
    "TOTAL",
    int(method_totals['Email']),
    int(method_totals['Call']),
    int(method_totals['Email + Call']),
    int(grand_total)
))
print("-" * 63)

# ============================================================================
# 5. TREND ANALYSIS: WEEK-OVER-WEEK CHANGES
# ============================================================================

print("\n" + "="*80)
print("WEEK-OVER-WEEK GROWTH ANALYSIS")
print("="*80)

for method in methods:
    print(f"\n{method}:")
    print("-" * 40)
    
    method_revenue = revenue_pivot[method]
    
    # Week 1 to Week 6 comparison
    week1_revenue = method_revenue.iloc[0]
    week6_revenue = method_revenue.iloc[-1]
    total_change = ((week6_revenue - week1_revenue) / week1_revenue) * 100
    
    print(f"  Week 1 revenue:     ${week1_revenue:>10,.0f}")
    print(f"  Week 6 revenue:     ${week6_revenue:>10,.0f}")
    print(f"  Total change:       {total_change:>+10.1f}%")
    
    # Calculate week-over-week growth rates
    wow_growth = method_revenue.pct_change() * 100
    avg_weekly_growth = wow_growth.mean()
    
    print(f"  Avg weekly growth:  {avg_weekly_growth:>+10.1f}%")
    
    # Trend interpretation
    if total_change > 100:
        trend = "🚀 Explosive growth"
    elif total_change > 20:
        trend = "📈 Strong growth"
    elif total_change > 0:
        trend = "✓ Positive growth"
    elif total_change > -20:
        trend = "⚠ Slight decline"
    else:
        trend = "❌ Significant decline"
    
    print(f"  Trend:              {trend}")

# ============================================================================
# 6. CROSSOVER POINT ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("METHOD PERFORMANCE CROSSOVER ANALYSIS")
print("="*80)

# Find when Email + Call surpassed Email
email_revenue = revenue_pivot['Email']
email_call_revenue = revenue_pivot['Email + Call']

crossover_weeks = []
for week in revenue_pivot.index:
    if email_call_revenue[week] > email_revenue[week]:
        crossover_weeks.append(week)

if crossover_weeks:
    first_crossover = min(crossover_weeks)
    print(f"\n✓ Email + Call surpassed Email starting in Week {first_crossover}")
    print(f"\n  Week {first_crossover} comparison:")
    print(f"    Email:         ${email_revenue[first_crossover]:>10,.0f}")
    print(f"    Email + Call:  ${email_call_revenue[first_crossover]:>10,.0f}")
    print(f"    Difference:    ${email_call_revenue[first_crossover] - email_revenue[first_crossover]:>10,.0f}")
    print("\n  🔄 This marks the inflection point where sustainable methodology")
    print("     overtook the exhausting approach.")
else:
    print("\n⚠ Email + Call never surpassed Email during the 6-week period")

# ============================================================================
# 7. MARKET SHARE EVOLUTION
# ============================================================================

print("\n" + "="*80)
print("REVENUE MARKET SHARE BY WEEK")
print("="*80)

print("\n{:<8} {:>12} {:>12} {:>15}".format('Week', 'Email %', 'Call %', 'Email + Call %'))
print("-" * 52)

for week in sorted(revenue_pivot.index):
    week_total = revenue_pivot.loc[week].sum()
    email_pct = (revenue_pivot.loc[week, 'Email'] / week_total) * 100
    call_pct = (revenue_pivot.loc[week, 'Call'] / week_total) * 100
    email_call_pct = (revenue_pivot.loc[week, 'Email + Call'] / week_total) * 100
    
    print("{:<8} {:>11.1f}% {:>11.1f}% {:>14.1f}%".format(
        f"Week {week}",
        email_pct,
        call_pct,
        email_call_pct
    ))

# Week 1 vs Week 6 market share shift
print("\n" + "="*80)
print("MARKET SHARE SHIFT: WEEK 1 vs WEEK 6")
print("="*80)

week1_total = revenue_pivot.iloc[0].sum()
week6_total = revenue_pivot.iloc[-1].sum()

print("\n{:<15} {:>12} {:>12} {:>12}".format('Method', 'Week 1', 'Week 6', 'Change'))
print("-" * 54)

for method in methods:
    week1_pct = (revenue_pivot.iloc[0][method] / week1_total) * 100
    week6_pct = (revenue_pivot.iloc[-1][method] / week6_total) * 100
    change = week6_pct - week1_pct
    
    print("{:<15} {:>11.1f}% {:>11.1f}% {:>+11.1f}%".format(
        method,
        week1_pct,
        week6_pct,
        change
    ))

# ============================================================================
# 8. VISUALIZATION: REVENUE TRENDS OVER TIME
# ============================================================================

print("\n" + "="*80)
print("GENERATING VISUALIZATION: TEMPORAL TRENDS")
print("="*80)

fig, ax = plt.subplots(figsize=(12, 7))

# Plot revenue trends for each method
for method in methods:
    method_data = revenue_by_week[revenue_by_week['sales_method'] == method]
    
    ax.plot(
        method_data['week'],
        method_data['revenue'],
        marker='o',
        linewidth=2.5,
        markersize=8,
        label=method,
        color=COLOR_MAP[method]
    )
    
    # Add trend line (linear regression)
    z = np.polyfit(method_data['week'], method_data['revenue'], 1)
    p = np.poly1d(z)
    ax.plot(
        method_data['week'],
        p(method_data['week']),
        linestyle='--',
        linewidth=1,
        color=COLOR_MAP[method],
        alpha=0.5
    )

# Styling
ax.set_title('Total Revenue by Week and Method', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Week', fontsize=12, fontweight='bold')
ax.set_ylabel('Total Revenue ($)', fontsize=12, fontweight='bold')
ax.legend(title='Sales Method', fontsize=10, loc='best')
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_xticks(range(1, 7))

# Format y-axis with dollar signs and commas
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${int(x):,}'))

# Add annotation for crossover point
if crossover_weeks:
    crossover_week = first_crossover
    crossover_value = email_call_revenue[crossover_week]
    ax.annotate(
        'Crossover Point',
        xy=(crossover_week, crossover_value),
        xytext=(crossover_week - 0.5, crossover_value + 20000),
        arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
        fontsize=10,
        fontweight='bold',
        color='red'
    )

plt.tight_layout()

# Save figure
output_path = '../visualizations/3_Total_Revenue_by_Week_and_Method.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✓ Visualization saved: {output_path}")

plt.show()

# ============================================================================
# 9. KEY INSIGHTS
# ============================================================================

print("\n" + "="*80)
print("KEY INSIGHTS")
print("="*80)

print("""
Temporal Performance Summary:
----------------------------
1. The Dramatic Reversal:
   - Week 1: Email dominated (84% market share)
   - Week 6: Email + Call dominated (77% market share)
   - Email collapsed by -89.7% over 6 weeks
   - Email + Call grew by +558% over 6 weeks

2. Sustainability Patterns:
   - Email + Call: Consistent upward trajectory (+76.7% per-customer improvement)
   - Email: Classic pipeline exhaustion (peaked Week 1, declined sharply)
   - Call: Consistently poor, no learning curve benefits

3. The Crossover Point:
   - Week 5: Email + Call surpassed Email for the first time
   - This marks inflection where sustainable beats exhausting

4. Learning Curve Evidence:
   - Email + Call improves as team gains experience ($129 → $228 per customer)
   - Email declines as high-intent prospects exhaust
   - Call shows no improvement (indicates fundamental method flaw, not execution)

Business Implications:
---------------------
📧 Email: Works for EXISTING customers who know your brand
   - Peaks immediately (early adopters)
   - Unsustainable for new customer acquisition
   - Best for re-engagement and upselling

📞 Call: Fails consistently across all weeks
   - No improvement despite 6 weeks of practice
   - Fundamental resistance, not execution issue
   - Eliminate entirely

📧+📞 Email + Call: Grows stronger over time
   - Warm calling beats cold calling every week
   - Team skills compound (learning curve)
   - Sustainable for ongoing acquisition

Critical Takeaway:
-----------------
Email's steep decline proves it captures "low-hanging fruit" but exhausts quickly.
Email + Call's steady growth proves it builds sustainable customer relationships.

For NEW customer acquisition: Email + Call is the only sustainable approach.
For EXISTING customers: Email remains efficient for maintenance/upselling.

Next Analysis:
-------------
- 05_efficiency_analysis.py: Revenue per minute validates time investment
""")

print("="*80)
print("ANALYSIS COMPLETE")
print("="*80)

# ============================================================================
# TECHNICAL NOTES
# ============================================================================
"""
Time-Series Analysis Methods:
-----------------------------
- Aggregation: Weekly revenue totals by method
- Trend calculation: Week 1 to Week 6 percentage change
- Growth rates: Week-over-week percentage changes
- Crossover detection: When Email + Call > Email

Visualization Enhancements:
--------------------------
- Solid lines: Actual revenue data points
- Dashed lines: Linear trend lines (shows trajectory)
- Markers: Individual weekly data points
- Crossover annotation: Highlights critical inflection point

Statistical Observations:
------------------------
1. Email exhibits negative acceleration (decline worsens each week)
2. Email + Call exhibits positive acceleration (growth compounds)
3. Call exhibits flat trend (no learning effect)

This proves method effectiveness isn't just about initial results,
but about sustainability and improvement over time.

Business Context:
----------------
The temporal analysis reveals the critical difference between:

EXTRACTIVE methods (Email): Mine existing demand, exhaust quickly
GENERATIVE methods (Email + Call): Create demand, compound over time

Email works when customers already want your product (awareness exists).
Email + Call works when customers don't know they need your product yet.

For a new product line, generative methods are essential for sustainable growth.
"""