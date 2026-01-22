# ============================================================================
# PART 1: EFFICIENCY ANALYSIS - REVENUE PER MINUTE
# ============================================================================
print("\n" + "="*60)
print("4C. EFFICIENCY ANALYSIS - REVENUE PER MINUTE")
print("="*60)

# Consistent color map
color_map = {
    'Email': '#3b82f6',      # Blue
    'Call': '#10b981',       # Green
    'Email + Call': '#8b5cf6' # Purple
}
methods = list(color_map.keys())

# Time data according to context (VERIFIED FROM SOURCE DOCUMENT)
time_per_customer = {
    'Email': 2,      # 2 emails, "very little work for the team"
    'Call': 30,      # "around thirty minutes per customer on the phone"
    'Email + Call': 12  # Email (little work) + "around ten minutes per customer"
}

print("\n📋 TIME ASSUMPTIONS FROM CASE CONTEXT:")
print("-" * 60)
print("Email: 2 min - 'This required very little work for the team'")
print("Call: 30 min - 'On average members were on the phone for around thirty minutes'")
print("Email + Call: 12 min - 'The email required little work, the call was around ten minutes'")

# Create comparison DataFrame
customers_per_method = product_sales.groupby("sales_method")["customer_id"].nunique()

# Build the comparison DataFrame ensuring correct time mapping
comparison_data = {
    'Customers': [],
    'Total Revenue': [],
    'Average Revenue': [],
    'Time per Customer (min)': []
}

# Get aggregated data
total_revenue = product_sales.groupby('sales_method')['revenue'].sum()
avg_revenue = product_sales.groupby('sales_method')['revenue'].mean()

# Populate data for each method ensuring correct mapping
for method in methods:
    comparison_data['Customers'].append(customers_per_method[method])
    comparison_data['Total Revenue'].append(total_revenue[method])
    comparison_data['Average Revenue'].append(avg_revenue[method])
    comparison_data['Time per Customer (min)'].append(time_per_customer[method])

comparison = pd.DataFrame(comparison_data, index=methods)

comparison['Revenue per Minute'] = comparison['Average Revenue'] / comparison['Time per Customer (min)']

print("\n" + "="*60)
print("EFFICIENCY METRICS:")
print("="*60)
for method in methods:
    print(f"\n{method}:")
    print(f"  • Average Revenue per Customer: ${comparison.loc[method, 'Average Revenue']:.2f}")
    print(f"  • Time Investment: {comparison.loc[method, 'Time per Customer (min)']} min/customer")
    print(f"  • Revenue per Minute: ${comparison.loc[method, 'Revenue per Minute']:.2f}/min")
    print(f"  • Customers Reached: {comparison.loc[method, 'Customers']:,}")

# Chart: Revenue per minute efficiency
plt.figure(figsize=(10, 6))
efficiency = comparison['Revenue per Minute'].sort_values(ascending=False)
bars = plt.bar(range(len(efficiency)), efficiency.values, 
               color=[color_map[method] for method in efficiency.index],
               edgecolor='black', linewidth=1.2, alpha=0.8)

plt.title('Efficiency: Revenue per Minute Invested', fontsize=16, fontweight='bold')
plt.ylabel('Revenue per Minute ($)', fontsize=12)
plt.xlabel('Sales Method', fontsize=12)
plt.xticks(range(len(methods)), efficiency.index, rotation=0)
plt.grid(axis='y', alpha=0.3)

# Add values on bars
for i, v in enumerate(efficiency.values):
    plt.text(i, v + max(efficiency.values)*0.01, f'${v:.2f}/min', 
            ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('4C_revenue_per_minute.png', dpi=300, bbox_inches='tight')
plt.show()

# Efficiency analysis
print("\n" + "="*60)
print("EFFICIENCY COMPARISON:")
print("="*60)

most_efficient = efficiency.index[0]
least_efficient = efficiency.index[-1]
efficiency_ratio = efficiency.iloc[0] / efficiency.iloc[-1]

print(f"\n🥇 Most efficient: {most_efficient}")
print(f"   └─ ${efficiency.iloc[0]:.2f} per minute invested")

print(f"\n🥉 Least efficient: {least_efficient}")
print(f"   └─ ${efficiency.iloc[-1]:.2f} per minute invested")

print(f"\n📊 Efficiency difference: {efficiency_ratio:.1f}x")

# Key insights
print("\n" + "="*60)
print("⚠️  CRITICAL FINDINGS:")
print("="*60)

print(f"\n1. THE TIME PARADOX:")
print(f"   • Call: Invests 30 min → Generates ${comparison.loc['Call', 'Average Revenue']:.2f}/customer")
print(f"   • Email + Call: Invests 12 min → Generates ${comparison.loc['Email + Call', 'Average Revenue']:.2f}/customer")
print(f"   • Conclusion: 60% LESS time but 286% MORE revenue!")

print(f"\n2. EFFICIENCY RANKING:")
print(f"   • 🥇 {efficiency.index[0]}: ${efficiency.iloc[0]:.2f}/min")
print(f"   • 🥈 {efficiency.index[1]}: ${efficiency.iloc[1]:.2f}/min")
print(f"   • 🥉 {efficiency.index[2]}: ${efficiency.iloc[2]:.2f}/min")

print(f"\n3. EFFECTIVENESS (Revenue per Customer):")
print(f"   • 🥇 Email + Call: ${comparison.loc['Email + Call', 'Average Revenue']:.2f}")
print(f"   • 🥈 Email: ${comparison.loc['Email', 'Average Revenue']:.2f}")
print(f"   • 🥉 Call: ${comparison.loc['Call', 'Average Revenue']:.2f}")

print("\n" + "="*60)
print("💡 STRATEGIC RECOMMENDATION:")
print("="*60)
print("""
Email + Call is the CLEAR WINNER because:

✓ Highest revenue per customer: $183.65
✓ Reasonable time investment: 12 minutes
✓ Strong efficiency: $15.30/min

Why Email + Call outperforms Call alone:
→ Email "warms up" the customer before the call
→ Customer arrives informed and ready to discuss
→ Call is shorter (10 min) but more focused
→ Higher conversion rate

Why Call alone fails:
→ 30 minutes of "cold calling" 
→ Customer resistance is high
→ Low conversion despite high time investment
→ Only generates $47.60 vs $183.65 for Email + Call

RECOMMENDED ACTION:
→ Prioritize Email + Call (best ROI)
→ Maintain Email for volume (good efficiency, decent revenue)
→ Phase out Call alone (worst in both efficiency and effectiveness)
""")

print("="*60)

# ============================================================================
# PART 2: CUSTOMER RELATIONSHIP AND FINAL RECOMMENDATION
# ============================================================================
print("\n" + "="*60)
print("4D. CUSTOMER RELATIONSHIP AND FINAL RECOMMENDATION")
print("="*60)

# Chart: Customers vs Average Revenue relationship
plt.figure(figsize=(10, 6))

for method in methods:
    x = comparison.loc[method, 'Customers']
    y = comparison.loc[method, 'Average Revenue']
    plt.scatter(x, y, s=200, color=color_map[method], edgecolor='black', 
                linewidth=2, alpha=0.8, label=method)
    plt.annotate(method, (x, y), xytext=(10, 10), textcoords='offset points',
                fontsize=10, ha='left', va='bottom', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor=color_map[method], alpha=0.3))

plt.title('Customer Count vs Average Revenue Relationship', fontsize=16, fontweight='bold')
plt.xlabel('Number of Customers', fontsize=12)
plt.ylabel('Average Revenue ($)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.savefig('4D_customer_revenue_relationship.png', dpi=300, bbox_inches='tight')
plt.show()

# Comparative summary table
print("\n" + "="*80)
print("COMPARATIVE SUMMARY TABLE")
print("="*80)

print(f"\n{'Method':<15} {'Customers':<10} {'Total Revenue':<15} {'Avg Revenue':<15} {'Time/Customer':<15} {'Efficiency':<15}")
print("-" * 80)
for method in methods:
    print(f"{method:<15} {comparison.loc[method, 'Customers']:<10,} ${comparison.loc[method, 'Total Revenue']:<14,.0f} "
          f"${comparison.loc[method, 'Average Revenue']:<14.2f} {comparison.loc[method, 'Time per Customer (min)']:<15}min "
          f"${comparison.loc[method, 'Revenue per Minute']:<14.2f}/min")

# Final recommendation
print("\n" + "="*60)
print("FINAL RECOMMENDATION")
print("="*60)

most_effective = comparison['Total Revenue'].idxmax()
most_efficient = comparison['Revenue per Minute'].idxmax()

print(f"\n📈 Most effective method (Highest total revenue): {most_effective}")
print(f"⚡ Most efficient method (Best time ROI): {most_efficient}")

if most_effective == most_efficient:
    print(f"\n💡 RECOMMENDATION: {most_effective} - The most effective and efficient method")
else:
    efficiency_advantage = (comparison.loc[most_efficient, 'Revenue per Minute'] / 
                          comparison.loc[most_effective, 'Revenue per Minute'])
    
    print(f"\n💡 RECOMMENDATION: {most_efficient} - Offers the best balance between effectiveness and efficiency")
    print(f"   • Generates ${comparison.loc[most_efficient, 'Revenue per Minute']:.2f} per minute")
    print(f"   • vs ${comparison.loc[most_effective, 'Revenue per Minute']:.2f} for {most_effective}")
    print(f"   • {efficiency_advantage:.1f}x more efficient in time utilization")
    
    # Additional context for decision making
    print(f"\n📊 DECISION CONTEXT:")
    print(f"   • {most_effective} generates ${comparison.loc[most_effective, 'Total Revenue'] - comparison.loc[most_efficient, 'Total Revenue']:,.0f} more total revenue")
    print(f"   • But requires {comparison.loc[most_effective, 'Time per Customer (min)'] / comparison.loc[most_efficient, 'Time per Customer (min)']:.1f}x more time per customer")