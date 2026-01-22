# Consistent color map
color_map = {
    'Email': '#3b82f6',      # Blue
    'Call': '#10b981',       # Green
    'Email + Call': '#8b5cf6' # Purple
}

methods = list(color_map.keys())

# Revenue by week and method
revenue_by_week = product_sales.groupby(['week', 'sales_method'])['revenue'].sum().reset_index()

# Create pivot table for better visualization
revenue_pivot = revenue_by_week.pivot(index='week', columns='sales_method', values='revenue')
revenue_pivot = revenue_pivot[methods]  # Order according to color_map

print("\nTOTAL REVENUE BY WEEK AND METHOD ($):")
print("-" * 50)
print(f"{'Week':<8} {'Email':<12} {'Call':<12} {'Email + Call':<15} {'Total':<12}")
print("-" * 50)

# Calculate and display formatted table
for week in sorted(revenue_by_week['week'].unique()):
    week_data = revenue_pivot.loc[week]
    week_total = week_data.sum()
    
    print(f"{week:<8} ${week_data['Email']:>10,.0f} ${week_data['Call']:>10,.0f} ${week_data['Email + Call']:>13,.0f} ${week_total:>10,.0f}")

# Totals by method
print("-" * 50)
method_totals = revenue_pivot.sum()
grand_total = method_totals.sum()
print(f"{'TOTAL':<8} ${method_totals['Email']:>10,.0f} ${method_totals['Call']:>10,.0f} ${method_totals['Email + Call']:>13,.0f} ${grand_total:>10,.0f}")

# Chart: Total revenue by week and method (line chart)
plt.figure(figsize=(10, 6))

for method in methods:
    data = revenue_by_week[revenue_by_week['sales_method'] == method]
    plt.plot(data['week'], data['revenue'], marker='o', linewidth=2.5, 
             label=method, color=color_map[method], markersize=8)

plt.title('Total Revenue by Week and Method', fontsize=16, fontweight='bold')
plt.xlabel('Week', fontsize=12)
plt.ylabel('Total Revenue ($)', fontsize=12)
plt.legend(title='Method', fontsize=10)
plt.grid(True, alpha=0.3)
plt.xticks(range(1, 7))

plt.tight_layout()
plt.savefig('3_Total_Revenue_by_Week_and_Method.png', dpi=300, bbox_inches='tight')
plt.show()