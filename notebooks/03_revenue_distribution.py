# ============================================================================
# QUESTION 2: Revenue Distribution by Sales Method - Histograms
# ============================================================================
print("\n" + "="*60)
print("REVENUE DISTRIBUTION BY SALES METHOD - HISTOGRAMS")
print("="*60)

# Consistent color map
color_map = {
    'Email': '#3b82f6',      # Blue
    'Call': '#10b981',       # Green
    'Email + Call': '#8b5cf6' # Purple
}

methods = list(color_map.keys())

# Chart: Revenue distribution by method - Overlaid histograms
plt.figure(figsize=(10, 6))

for method in methods:
    method_data = product_sales[product_sales['sales_method'] == method]['revenue']
    plt.hist(method_data, bins=20, alpha=0.6, color=color_map[method], 
             edgecolor='black', linewidth=0.5, label=method)

plt.title('Revenue Distribution by Sales Method', fontsize=16, fontweight='bold')
plt.xlabel('Revenue ($)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.legend()
plt.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('2D_revenue_by_method_histograms.png', dpi=300, bbox_inches='tight')
plt.show()

# Comparative analysis
print(f"\nCOMPARATIVE ANALYSIS BY SALES METHOD:")
print("-" * 45)

# Calculate relative performance
overall_mean = product_sales['revenue'].mean()
print(f"Overall mean revenue: ${overall_mean:.2f}")

for method in methods:
    method_data = product_sales[product_sales['sales_method'] == method]['revenue']
    method_mean = method_data.mean()
    performance_vs_overall = ((method_mean - overall_mean) / overall_mean) * 100
    
    print(f"\n{method}:")
    print(f"  Mean revenue: ${method_mean:.2f}")
    print(f"  Performance vs overall: {performance_vs_overall:+.1f}%")
    print(f"  Customer share: {len(method_data)/len(product_sales)*100:.1f}% of total")

# Best performing method
best_method = max(methods, key=lambda x: product_sales[product_sales['sales_method'] == x]['revenue'].mean())
best_mean = product_sales[product_sales['sales_method'] == best_method]['revenue'].mean()
print(f"\n🏆 Best performing method: {best_method} (${best_mean:.2f} average revenue)")

# ============================================================================
# QUESTION 2: Revenue Distribution by Sales Method - Boxplots
# ============================================================================
print("\n" + "="*60)
print("REVENUE DISTRIBUTION BY SALES METHOD - BOXPLOTS")
print("="*60)

# Consistent color map
color_map = {
    'Email': '#3b82f6',      # Blue
    'Call': '#10b981',       # Green
    'Email + Call': '#8b5cf6' # Purple
}

methods = list(color_map.keys())

# Chart: Revenue by sales method - Boxplots
plt.figure(figsize=(10, 6))

for i, method in enumerate(methods):
    method_data = product_sales[product_sales['sales_method'] == method]['revenue']
    
    plt.boxplot(method_data, positions=[i], widths=0.6, patch_artist=True,
               boxprops=dict(facecolor=color_map[method], alpha=0.7),
               medianprops=dict(color='yellow', linewidth=2),
               whiskerprops=dict(linewidth=1.5),
               capprops=dict(linewidth=1.5),
               flierprops=dict(marker='o', markersize=4, alpha=0.6))

plt.title('Revenue Distribution by Sales Method', fontsize=16, fontweight='bold')
plt.ylabel('Revenue ($)', fontsize=12)
plt.xlabel('Sales Method', fontsize=12)
plt.xticks(range(len(methods)), methods, rotation=45)
plt.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('2C_revenue_by_method_boxplots.png', dpi=300, bbox_inches='tight')
plt.show()

# Statistics for boxplot analysis
print(f"\nREVENUE STATISTICS BY SALES METHOD:")
print("-" * 45)
for method in methods:
    method_data = product_sales[product_sales['sales_method'] == method]['revenue']
    
    print(f"\n{method}:")
    print(f"  Customers: {len(method_data):,}")
    print(f"  Mean: ${method_data.mean():.2f}")
    print(f"  Median: ${method_data.median():.2f}")
    print(f"  Std Dev: ${method_data.std():.2f}")
    print(f"  Range: ${method_data.min():.2f} - ${method_data.max():.2f}")
    
    # IQR analysis
    Q1 = method_data.quantile(0.25)
    Q3 = method_data.quantile(0.75)
    IQR = Q3 - Q1
    print(f"  IQR: ${IQR:.2f} (Q1: ${Q1:.2f}, Q3: ${Q3:.2f})")