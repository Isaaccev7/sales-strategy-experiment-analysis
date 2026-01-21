print("\n" + "="*60)
print("1. CUSTOMERS BY SALES METHOD")
print("="*60)

customers_per_method = product_sales.groupby("sales_method")["customer_id"].nunique().sort_values(ascending=False)
print("\nNumber of unique customers by method:")
print(customers_per_method)
print(f"\nTotal customers: {product_sales['customer_id'].nunique()}")

# Graph 1: Customers by method
fig, ax = plt.subplots(figsize=(10, 6))

# Use the same colors as in previous graphs
color_map = {
    'Email': '#3b82f6',      # Blue
    'Call': '#10b981',       # Green
    'Email + Call': '#8b5cf6' # Purple
}
    


# Order methods according to color_map
customers_per_method = customers_per_method.reindex(color_map.keys())

bars = customers_per_method.plot(kind='bar', ax=ax, color=[color_map[method] for method in customers_per_method.index], 
                                 edgecolor='black', linewidth=1.2, alpha=0.8)

ax.set_title('Number of Customers by Sales Method', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Sales Method', fontsize=12, fontweight='bold')
ax.set_ylabel('Number of Customers', fontsize=12, fontweight='bold')
ax.set_xticklabels(customers_per_method.index, rotation=45)
ax.grid(axis='y', alpha=0.3)

# Add values on bars
for i, v in enumerate(customers_per_method.values):
    ax.text(i, v + max(customers_per_method.values)*0.01, f'{v:,}', 
            ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('1_customers_by_method.png', dpi=300, bbox_inches='tight')
plt.show()