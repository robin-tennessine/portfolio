"""
Generate sample retail data for portfolio demonstration
This script creates synthetic sales and customer data for analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_customer_data(n_customers=1000):
    """Generate synthetic customer data"""

    customer_ids = [f'CUST{str(i).zfill(6)}' for i in range(1, n_customers + 1)]

    # Demographics
    genders = np.random.choice(['M', 'F'], n_customers, p=[0.48, 0.52])
    ages = np.random.normal(35, 12, n_customers).astype(int)
    ages = np.clip(ages, 18, 75)

    # Registration dates (last 3 years)
    start_date = datetime.now() - timedelta(days=1095)
    registration_dates = [start_date + timedelta(days=random.randint(0, 1095))
                          for _ in range(n_customers)]

    # Customer segments
    segments = np.random.choice(
        ['Premium', 'Regular', 'Occasional', 'New'],
        n_customers,
        p=[0.15, 0.35, 0.35, 0.15]
    )

    # Cities (Thailand context for Jaymart)
    cities = np.random.choice(
        ['Bangkok', 'Chiang Mai', 'Phuket', 'Pattaya', 'Khon Kaen', 'Hat Yai'],
        n_customers,
        p=[0.45, 0.15, 0.10, 0.10, 0.10, 0.10]
    )

    # Lifetime value based on segment
    segment_ltv = {
        'Premium': (50000, 150000),
        'Regular': (15000, 50000),
        'Occasional': (3000, 15000),
        'New': (500, 5000)
    }

    lifetime_values = []
    for seg in segments:
        ltv_min, ltv_max = segment_ltv[seg]
        lifetime_values.append(np.random.uniform(ltv_min, ltv_max))

    customer_df = pd.DataFrame({
        'customer_id': customer_ids,
        'gender': genders,
        'age': ages,
        'city': cities,
        'registration_date': registration_dates,
        'customer_segment': segments,
        'lifetime_value': np.round(lifetime_values, 2)
    })

    return customer_df


def generate_sales_data(customer_df, n_transactions=10000):
    """Generate synthetic sales transaction data"""

    # Product categories (mobile phones and cafe items for Jaymart Mobile & Casa Lapin)
    products = [
        # Mobile products
        {'category': 'Smartphone', 'product': 'iPhone 14', 'price': 32900},
        {'category': 'Smartphone', 'product': 'Samsung Galaxy S23', 'price': 28900},
        {'category': 'Smartphone', 'product': 'OPPO Reno8', 'price': 15990},
        {'category': 'Accessories', 'product': 'Phone Case', 'price': 390},
        {'category': 'Accessories', 'product': 'Screen Protector', 'price': 290},
        {'category': 'Accessories', 'product': 'Wireless Charger', 'price': 1290},
        # Cafe products
        {'category': 'Coffee', 'product': 'Americano', 'price': 95},
        {'category': 'Coffee', 'product': 'Cappuccino', 'price': 110},
        {'category': 'Coffee', 'product': 'Latte', 'price': 115},
        {'category': 'Beverage', 'product': 'Green Tea', 'price': 85},
        {'category': 'Food', 'product': 'Sandwich', 'price': 145},
        {'category': 'Food', 'product': 'Croissant', 'price': 95},
    ]

    # Store locations
    stores = ['Central World', 'Siam Paragon', 'Terminal 21', 'MBK Center',
              'Central Chiang Mai', 'Central Festival Phuket']

    # Generate transactions
    transactions = []
    start_date = datetime.now() - timedelta(days=365)

    for i in range(n_transactions):
        transaction_id = f'TXN{str(i + 1).zfill(8)}'

        # Random customer (weighted toward regular customers)
        customer = customer_df.sample(1).iloc[0]

        # Transaction date (more recent transactions have higher probability)
        days_ago = int(np.random.exponential(90))
        days_ago = min(days_ago, 365)
        transaction_date = datetime.now() - timedelta(days=days_ago)

        # Random product
        product = random.choice(products)

        # Quantity (mostly 1, sometimes 2-3 for accessories/food)
        if product['category'] in ['Accessories', 'Food', 'Coffee', 'Beverage']:
            quantity = random.choices([1, 2, 3], weights=[0.7, 0.2, 0.1])[0]
        else:
            quantity = 1

        # Store location
        store = random.choice(stores)

        # Calculate revenue
        revenue = product['price'] * quantity

        transactions.append({
            'transaction_id': transaction_id,
            'transaction_date': transaction_date,
            'customer_id': customer['customer_id'],
            'product_category': product['category'],
            'product_name': product['product'],
            'quantity': quantity,
            'unit_price': product['price'],
            'revenue': revenue,
            'store_location': store
        })

    sales_df = pd.DataFrame(transactions)
    sales_df = sales_df.sort_values('transaction_date').reset_index(drop=True)

    return sales_df


if __name__ == '__main__':
    print("Generating sample data...")

    # Generate customer data
    print("Creating customer data...")
    customers = generate_customer_data(n_customers=1000)
    customers.to_csv('customer_data.csv', index=False)
    print(f"Generated {len(customers)} customers")

    # Generate sales data
    print("Creating sales transaction data...")
    sales = generate_sales_data(customers, n_transactions=10000)
    sales.to_csv('sales_data.csv', index=False)
    print(f"Generated {len(sales)} transactions")

    print("\nData generation complete!")
    print(f"Files created:")
    print("  - customer_data.csv")
    print("  - sales_data.csv")

    # Display sample data
    print("\n--- Customer Data Sample ---")
    print(customers.head())
    print("\n--- Sales Data Sample ---")
    print(sales.head())

    # Display summary statistics
    print("\n--- Summary Statistics ---")
    print(f"Total Revenue: ${sales['revenue'].sum():,.2f}")
    print(f"Average Transaction Value: ${sales['revenue'].mean():,.2f}")
    print(f"Date Range: {sales['transaction_date'].min()} to {sales['transaction_date'].max()}")
