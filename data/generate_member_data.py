"""
Generate sample member transaction data for Sankey visualization
Mimics retail member database with yearly transactions
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
NUM_MEMBERS = 2000
START_YEAR = 2021
END_YEAR = 2025
PRODUCT_CATEGORIES = ['Coffee', 'Pastry', 'Sandwich', 'Beverage', 'Dessert', 'Merchandise']

def generate_member_master():
    """Generate master member data with demographics"""

    first_names_male = ['John', 'Michael', 'David', 'James', 'Robert', 'William', 'Richard',
                        'Thomas', 'Christopher', 'Daniel', 'Matthew', 'Anthony', 'Mark']
    first_names_female = ['Mary', 'Jennifer', 'Linda', 'Patricia', 'Elizabeth', 'Susan',
                          'Jessica', 'Sarah', 'Karen', 'Nancy', 'Lisa', 'Betty', 'Margaret']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller',
                  'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Wilson', 'Anderson']

    members = []

    for i in range(NUM_MEMBERS):
        member_id = f'M{str(i+1).zfill(6)}'
        gender = random.choice(['M', 'F'])

        if gender == 'M':
            first_name = random.choice(first_names_male)
        else:
            first_name = random.choice(first_names_female)

        last_name = random.choice(last_names)

        # Generate birthdate (age between 20-65)
        age = random.randint(20, 65)
        birthdate = datetime.now() - timedelta(days=age*365 + random.randint(0, 365))

        # Determine generation based on birth year
        birth_year = birthdate.year
        if birth_year >= 1997:
            generation = 'Gen Z'
        elif birth_year >= 1981:
            generation = 'Millennial'
        elif birth_year >= 1965:
            generation = 'Gen X'
        else:
            generation = 'Boomer'

        # Age range
        if age < 25:
            age_range = '18-24'
        elif age < 35:
            age_range = '25-34'
        elif age < 45:
            age_range = '35-44'
        elif age < 55:
            age_range = '45-54'
        else:
            age_range = '55+'

        # Mobile number
        mobile_no = f'08{random.randint(10000000, 99999999)}'

        # UUID
        uuid = f'{random.randint(10000000, 99999999)}-{random.randint(1000, 9999)}'

        # Total points (loyalty points)
        total_point = random.randint(0, 10000)

        # First purchase date (registration)
        first_purchase_year = random.randint(START_YEAR, END_YEAR)
        first_purchase_date = datetime(first_purchase_year, random.randint(1, 12), random.randint(1, 28))

        members.append({
            'Member_ID': member_id,
            'FIRST_NAME': first_name,
            'LAST_NAME': last_name,
            'GENDER': gender,
            'BIRTHDATE': birthdate.strftime('%Y-%m-%d'),
            'Age_Range': age_range,
            'Generation': generation,
            'MOBILE_NO': mobile_no,
            'UUID': uuid,
            'Total_point': total_point,
            'FirstPurchaseDate': first_purchase_date.strftime('%Y-%m-%d')
        })

    return pd.DataFrame(members)


def generate_yearly_transactions(members_df):
    """Generate yearly transaction data for each member"""

    transactions = []

    for _, member in members_df.iterrows():
        member_id = member['Member_ID']
        first_purchase = pd.to_datetime(member['FirstPurchaseDate'])

        # Determine member engagement level (affects transaction frequency)
        engagement_level = np.random.choice(['low', 'medium', 'high', 'very_high'],
                                           p=[0.3, 0.4, 0.2, 0.1])

        # Generate transactions for each year from first purchase to end
        for year in range(first_purchase.year, END_YEAR + 1):
            # Skip if year is before first purchase
            if year < first_purchase.year:
                continue

            # Determine if customer is active this year (some churn over time)
            years_since_first = year - first_purchase.year
            churn_probability = min(0.05 + (years_since_first * 0.05), 0.4)

            if random.random() < churn_probability:
                # Customer churned, decide if they come back
                if random.random() < 0.2:  # 20% reactivation chance
                    is_active = True
                else:
                    continue
            else:
                is_active = True

            if is_active:
                # Determine number of transactions based on engagement
                if engagement_level == 'very_high':
                    txn_count = random.randint(20, 50)
                elif engagement_level == 'high':
                    txn_count = random.randint(10, 20)
                elif engagement_level == 'medium':
                    txn_count = random.randint(5, 10)
                else:
                    txn_count = random.randint(1, 5)

                # Calculate total metrics for the year
                total_qty = txn_count * random.randint(1, 3)
                avg_spend_per_txn = random.uniform(50, 300)
                total_spend = txn_count * avg_spend_per_txn

                # Generate last transaction date for the year
                if year == END_YEAR:
                    # For current year, transactions could be recent
                    max_month = min(12, datetime.now().month)
                    max_day = 28
                else:
                    max_month = 12
                    max_day = 28

                max_sale_date = datetime(year, max_month, random.randint(1, max_day))

                # Most frequent product category
                mode_product_category = random.choice(PRODUCT_CATEGORIES)

                transactions.append({
                    'Member_ID': member_id,
                    'YEAR': str(year),
                    'TotalTxn': txn_count,
                    'TotalQty': total_qty,
                    'TotalSpend': round(total_spend, 2),
                    'MaxSaleDate': max_sale_date.strftime('%Y-%m-%d'),
                    'Mode_ProductCategory': mode_product_category
                })

    return pd.DataFrame(transactions)


def main():
    """Generate and save member data"""

    print("Generating member master data...")
    members_df = generate_member_master()
    print(f"Generated {len(members_df)} members")

    print("\nGenerating yearly transaction data...")
    transactions_df = generate_yearly_transactions(members_df)
    print(f"Generated {len(transactions_df)} member-year records")

    # Save to CSV
    members_df.to_csv('member_master.csv', index=False)
    transactions_df.to_csv('member_segment_yearly.csv', index=False)

    print("\nFiles saved:")
    print("- member_master.csv")
    print("- member_segment_yearly.csv")

    print("\nMember Master Sample:")
    print(members_df.head())

    print("\nTransaction Data Sample:")
    print(transactions_df.head(10))

    print("\nYearly Transaction Distribution:")
    print(transactions_df.groupby('YEAR').size())


if __name__ == '__main__':
    main()
