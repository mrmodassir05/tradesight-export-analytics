import os
import pandas as pd
import numpy as np

print("--- TradeSight Export Analytics Pipeline Starting ---")

def load_file_from_anywhere(file_name):
    possible_locations = [
        os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop", "python"),
        os.path.join(os.path.expanduser("~"), "Desktop", "python"),
        os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop"),
        os.path.join(os.path.expanduser("~"), "Desktop"),
        os.path.join(os.path.expanduser("~"), "Downloads"),
        os.getcwd()
    ]
    
    for folder in possible_locations:
        full_path = os.path.join(folder, file_name)
        if os.path.exists(full_path):
            print(f"Found and loaded: {file_name}")
            df = pd.read_csv(full_path)
            df.columns = df.columns.str.strip().str.lower()
            return df
            
    raise FileNotFoundError(f"Could not locate {file_name} in target paths.")

# === WEEK 3: DATA INGESTION & PIPELINE ===
orders = load_file_from_anywhere('da_b2b_orders.csv')
catalogue = load_file_from_anywhere('da_product_catalogue.csv')
customers = load_file_from_anywhere('da_customer_profiles.csv')

# Column align parameters
if 'customer_id' not in orders.columns and 'buyer_id' in orders.columns:
    orders.rename(columns={'buyer_id': 'customer_id'}, inplace=True)
if 'customer_id' not in customers.columns and 'customer_id' in customers.columns:
    pass

# Structural data merge based on parameters
df_merged = pd.merge(orders, catalogue, on='category', how='left', suffixes=('', '_cat'))
final_df = pd.merge(df_merged, customers, on='customer_id', how='left', suffixes=('', '_cust'))
print("\n Data pipeline established successfully!")

# === WEEK 6: ADVANCED EXPORT ANALYTICS ===
df = final_df 

# 1. Client Profitability Ranking Mappings
if 'cost_price' in df.columns and 'sales_price' in df.columns:
    df['net_profit'] = (df['sales_price'] - df['cost_price']) * df['quantity']
elif 'total_value_inr' in df.columns:
    df['net_profit'] = df['total_value_inr'] * 0.15 
elif 'total_value' in df.columns:
    df['net_profit'] = df['total_value'] * 0.15 
else:
    df['net_profit'] = 0.0

client_col = 'customer_name' if 'customer_name' in df.columns else 'customer_id'
client_ranking = df.groupby(client_col)['net_profit'].sum().sort_values(ascending=False)

# 2. 12-Country Performance Analysis Configuration
if 'country' in df.columns:
    country_col = 'country'
elif 'city' in df.columns:
    country_col = 'city'
else:
    country_col = [col for col in df.columns if 'country' in col or 'city' in col or 'region' in col]
    country_col = country_col if country_col else df.columns[-1]

val_col = 'total_value_inr' if 'total_value_inr' in df.columns else ('total_value' if 'total_value' in df.columns else 'net_profit')

country_performance = df.groupby(country_col).agg(
    total_sales_value=(val_col, 'sum'),
    total_orders_count=(val_col, 'count'),
    total_net_profit=('net_profit', 'sum')
).sort_values(by='total_net_profit', ascending=False)

# 3. Currency Impact Calculator (FX Analytics)
exchange_rates = {'USD': 84.0, 'EUR': 91.0, 'GBP': 108.0, 'INR': 1.0}
if 'currency' in df.columns:
    df['fx_rate'] = df['currency'].map(exchange_rates).fillna(1.0)
    df['value_in_inr'] = df[val_col] * df['fx_rate']

# 4. Compliance Tracking Logic Mappings
if 'delivery_days' in df.columns:
    df['compliance_flag'] = np.where(df['delivery_days'] > 7, 'Late Shipment', 'Compliant')
else:
    df['compliance_flag'] = np.where(df[val_col].isnull(), 'Flagged: Missing Info', 'Compliant')

# === PRINTING EXECUTIVE ANALYTICAL RESULTS ===
print("\n==============================================")
print("=== TOP 5 MOST PROFITABLE CLIENTS ===")
print(client_ranking.head())

print("\n=== COUNTRY PERFORMANCE SUMMARY ===")
print(country_performance.head(12))

print("\n=== COMPLIANCE EXCEPTION SUMMARY ===")
print(df['compliance_flag'].value_counts())
print("==============================================")

# Saving master dataset record
df.to_csv('tradesight_export_analytics_output.csv', index=False)
print("\n🚀 Week 6 Analysis Completed Successfully!")
print("File saved as: 'tradesight_export_analytics_output.csv'")



# Data from the provided image
data = {
    'order_id': ['B2B-00001', 'B2B-00002', 'B2B-00003', 'B2B-00004', 'B2B-00005', 'B2B-00006', 'B2B-00007', 'B2B-00008', 'B2B-00009', 'B2B-00010'],
    'buyer_id': ['BUY-0160', 'BUY-0019', 'BUY-0132', 'BUY-0031', 'BUY-0148', 'BUY-0012', 'BUY-0139', 'BUY-0018', 'BUY-0045', 'BUY-0118'],
    'category': ['Food Ingredients', 'Raw Materials', 'Chemicals', 'Electronic Components', 'Office Supplies', 'Packaging', 'Raw Materials', 'Textiles', 'Electronic Components', 'Industrial Machinery'],
    'order_date': ['22-11-2024', '02-06-2023', '24-01-2024', '29-09-2024', '11-01-2023', '30-04-2024', '05-12-2024', '26-10-2024', '27-10-2024', '12-08-2024'],
    'quantity_units': [4497, 2032, 4813, 1962, 2977, 4968, 775, 4746, 4797, 739],
    'total_value_inr': [20642039.46, 7185233.28, 17205368.01, 2935250.10, 780480.09, 22516665.12, 3615956.25, 21097251.42, 23598121.95, 3071853.03],
    'delivery_days': [4, 6, 13, 14, 35, 40, 38, 6, 36, 33],
    'net_profit': [3096305.92, 1077784.99, 2580805.20, 440287.51, 117072.01, 3377499.77, 542393.44, 3164587.71, 3539718.29, 460777.95],
    'compliance_flag': ['Compliant', 'Compliant', 'Late Shipment', 'Late Shipment', 'Late Shipment', 'Late Shipment', 'Late Shipment', 'Compliant', 'Late Shipment', 'Late Shipment']
}

df = pd.DataFrame(data)

# Calculate values
total_sales = df['total_value_inr'].sum()
total_profit = df['net_profit'].sum()
profit_margin = (total_profit / total_sales) * 100
total_orders = len(df)
unique_customers = df['buyer_id'].nunique()
# As there is no country column visible, we'll use category or assume unique countries based on context, but let's count unique categories for this sample
unique_categories = df['category'].nunique()
late_shipments = len(df[df['compliance_flag'] == 'Late Shipment'])
compliance_rate = (len(df[df['compliance_flag'] == 'Compliant']) / total_orders) * 100

print(f"Total Sales: {total_sales}")
print(f"Total Profit: {total_profit}")
print(f"Profit Margin: {profit_margin}%")
print(f"Total Orders: {total_orders}")
print(f"Unique Customers: {unique_customers}")
print(f"Unique Categories: {unique_categories}")
print(f"Late Shipments: {late_shipments}")
print(f"Compliance Rate: {compliance_rate}%")

df.to_excel('tradesight_master_report.xlsx', index=False)

# Fix: Save directly to your active OneDrive Desktop folder
final_file_path = r"C:\Users\modas\OneDrive\Desktop\tradesight_export_analytics_output.csv"
df.to_csv(final_file_path, index=False)
print(f"Success! Output file created on Desktop: {final_file_path}")

