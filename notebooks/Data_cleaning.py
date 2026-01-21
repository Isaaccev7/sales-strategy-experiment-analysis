# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Import the data
product_sales = pd.read_csv("product_sales.csv")

# Preview the DataFrame
product_sales

# 1. Clean up sales_method categories
product_sales["sales_method"] = product_sales["sales_method"].replace({
    "em + call": "Email + Call",
    "email": "Email"
})

# 2. Remove rows with empty revenue
product_sales.dropna(subset=['revenue'], inplace=True)

# 3. Verify results
print("Valores nulos después de la limpieza:")
print(product_sales.isnull().sum())
print("\nCategorías de sales_method:")
print(product_sales["sales_method"].value_counts())
print("-" * 25)
print(product_sales.nunique())
