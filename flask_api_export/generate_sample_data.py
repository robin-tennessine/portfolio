"""
Generate Sample Transaction Data for Portfolio Demonstration
Creates realistic transaction data for Jaymart Mobile and Casa Lapin
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def generate_thai_names(n):
    """Generate sample Thai names"""
    first_names = ['Somchai', 'Somsri', 'Niran', 'Naphat', 'Siriporn', 'Warit',
                   'Apinya', 'Chaiya', 'Duangjai', 'Jaturong', 'Kamon', 'Ladda',
                   'Manee', 'Narong', 'Orapin', 'Prasert', 'Ratchanee', 'Sakchai',
                   'Tawan', 'Udom', 'Vichit', 'Wanida', 'Yuttana', 'Achara']

    last_names = ['Phonpakdee', 'Suksawat', 'Thongkam', 'Rattana', 'Boonma',
                  'Chaiyaporn', 'Dechapol', 'Jiraporn', 'Kritsana', 'Methee',
                  'Nattapong', 'Paiboon', 'Rungruang', 'Sanitchai', 'Tanawat',
                  'Worawut', 'Yongyut', 'Anucha', 'Boonsong', 'Chatchai']

    names = []
    for _ in range(n):
        first = random.choice(first_names)
        last = random.choice(last_names)
        names.append(f"{first} {last}")

    return names


def generate_id_cards(n):
    """Generate sample Thai ID card numbers (13 digits)"""
    id_cards = []
    for _ in range(n):
        # Thai ID format: X-XXXX-XXXXX-XX-X
        id_card = ''.join([str(random.randint(0, 9)) for _ in range(13)])
        id_cards.append(id_card)
    return id_cards


def generate_passports(n):
    """Generate sample passport numbers"""
    passports = []
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for _ in range(n):
        if random.random() < 0.7:  # 70% have passport
            prefix = ''.join(random.choices(letters, k=2))
            number = ''.join([str(random.randint(0, 9)) for _ in range(7)])
            passports.append(f"{prefix}{number}")
        else:
            passports.append(None)
    return passports


def generate_emails(names):
    """Generate email addresses from names"""
    domains = ['gmail.com', 'hotmail.com', 'yahoo.com', 'outlook.com']
    emails = []

    for name in names:
        name_parts = name.lower().split()
        username = f"{name_parts[0]}.{name_parts[1]}{random.randint(1, 999)}"
        domain = random.choice(domains)
        emails.append(f"{username}@{domain}")

    return emails


def generate_phones(n):
    """Generate Thai phone numbers (08x-xxx-xxxx)"""
    phones = []
    prefixes = ['08', '09', '06']

    for _ in range(n):
        prefix = random.choice(prefixes)
        rest = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        phones.append(f"{prefix}{rest}")

    return phones


def generate_transactions(n_transactions=5000):
    """Generate sample transaction data"""

    print(f"Generating {n_transactions} sample transactions...")

    # Generate unique customers (fewer customers than transactions for repeat purchases)
    n_customers = int(n_transactions * 0.3)
    customer_ids = [f"CUST{str(i).zfill(6)}" for i in range(1, n_customers + 1)]

    # Generate customer master data
    customer_names = generate_thai_names(n_customers)
    id_cards = generate_id_cards(n_customers)
    passports = generate_passports(n_customers)
    emails = generate_emails(customer_names)
    phones = generate_phones(n_customers)

    # Business units and products
    business_units = {
        'Jaymart Mobile': {
            'products': ['iPhone 15 Pro', 'Samsung Galaxy S24', 'iPad Pro', 'AirPods Pro',
                        'Apple Watch', 'Samsung Tablet', 'Phone Accessories', 'Mobile Insurance'],
            'price_range': (500, 50000)
        },
        'Casa Lapin': {
            'products': ['Espresso', 'Cappuccino', 'Latte', 'Americano', 'Croissant',
                        'Sandwich', 'Cake', 'Smoothie', 'Coffee Beans'],
            'price_range': (50, 500)
        }
    }

    # Store locations
    locations = ['Bangkok - Siam', 'Bangkok - Asoke', 'Chiang Mai Central',
                 'Phuket - Patong', 'Pattaya Center', 'Bangkok - Thonglor',
                 'Bangkok - Sukhumvit', 'Bangkok - Silom']

    # Payment methods
    payment_methods = ['Credit Card', 'Debit Card', 'Cash', 'QR Payment', 'Bank Transfer']

    # Generate transactions
    transactions = []
    start_date = datetime.now() - timedelta(days=365)

    for i in range(n_transactions):
        # Random customer (some customers buy multiple times)
        customer_idx = random.choice(range(n_customers))

        # Random business unit
        bu_name = random.choice(list(business_units.keys()))
        bu_data = business_units[bu_name]

        # Random product from business unit
        product = random.choice(bu_data['products'])

        # Random price within range
        price_min, price_max = bu_data['price_range']
        unit_price = round(random.uniform(price_min, price_max), 2)

        # Quantity (mostly 1, sometimes more)
        quantity = random.choices([1, 2, 3], weights=[0.8, 0.15, 0.05])[0]

        # Calculate total
        subtotal = unit_price * quantity
        discount = round(subtotal * random.choice([0, 0.05, 0.10, 0.15]), 2)
        total_amount = subtotal - discount

        # Random date within last year
        transaction_date = start_date + timedelta(days=random.randint(0, 365))

        # Create transaction record
        transaction = {
            'transaction_id': f"TXN{str(i+1).zfill(8)}",
            'transaction_date': transaction_date.strftime('%Y-%m-%d'),
            'transaction_time': f"{random.randint(8, 20):02d}:{random.randint(0, 59):02d}",
            'customer_id': customer_ids[customer_idx],
            'customer_name': customer_names[customer_idx],
            'id_card': id_cards[customer_idx],
            'passport': passports[customer_idx],
            'email': emails[customer_idx],
            'phone': phones[customer_idx],
            'business_unit': bu_name,
            'store_location': random.choice(locations),
            'product_name': product,
            'product_category': 'Electronics' if bu_name == 'Jaymart Mobile' else 'F&B',
            'quantity': quantity,
            'unit_price': unit_price,
            'subtotal': subtotal,
            'discount': discount,
            'total_amount': total_amount,
            'payment_method': random.choice(payment_methods),
            'status': random.choices(['Completed', 'Pending', 'Cancelled'],
                                   weights=[0.9, 0.07, 0.03])[0]
        }

        transactions.append(transaction)

    # Create DataFrame
    df = pd.DataFrame(transactions)

    # Sort by date
    df = df.sort_values('transaction_date').reset_index(drop=True)

    print(f"✅ Generated {len(df)} transactions")
    print(f"   - Date range: {df['transaction_date'].min()} to {df['transaction_date'].max()}")
    print(f"   - Unique customers: {df['customer_id'].nunique()}")
    print(f"   - Business units: {df['business_unit'].unique()}")
    print(f"   - Total revenue: ฿{df['total_amount'].sum():,.2f}")

    return df


if __name__ == "__main__":
    # Generate data
    df = generate_transactions(5000)

    # Save to CSV
    output_file = 'sample_transactions.csv'
    df.to_csv(output_file, index=False)
    print(f"\n✅ Saved to {output_file}")

    # Show sample
    print("\nSample records (first 5):")
    print(df.head())

    print("\nSummary statistics:")
    print(df[['quantity', 'unit_price', 'total_amount']].describe())
