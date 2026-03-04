"""
ETL Pipeline for Retail Sales Data
===================================

This script demonstrates an end-to-end ETL (Extract, Transform, Load) pipeline
for processing retail sales and customer data.

Process:
1. EXTRACT: Load data from multiple sources (CSV files)
2. TRANSFORM: Clean, validate, and enrich the data
3. LOAD: Output analytics-ready datasets

Author: Data Analytics Portfolio
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import os
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('etl_pipeline.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class DataValidator:
    """
    Validates data quality and integrity
    """

    @staticmethod
    def validate_sales_data(df):
        """Validate sales data quality"""
        logger.info("Validating sales data...")

        issues = []

        # Check for required columns
        required_cols = ['transaction_id', 'customer_id', 'transaction_date', 'revenue']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            issues.append(f"Missing required columns: {missing_cols}")

        # Check for null values
        null_counts = df.isnull().sum()
        if null_counts.any():
            issues.append(f"Null values found: {null_counts[null_counts > 0].to_dict()}")

        # Check for negative revenue
        if 'revenue' in df.columns:
            negative_revenue = (df['revenue'] < 0).sum()
            if negative_revenue > 0:
                issues.append(f"Found {negative_revenue} records with negative revenue")

        # Check for duplicate transaction IDs
        if 'transaction_id' in df.columns:
            duplicates = df['transaction_id'].duplicated().sum()
            if duplicates > 0:
                issues.append(f"Found {duplicates} duplicate transaction IDs")

        if issues:
            logger.warning(f"Data validation issues: {issues}")
            return False, issues
        else:
            logger.info("Data validation passed!")
            return True, []

    @staticmethod
    def validate_customer_data(df):
        """Validate customer data quality"""
        logger.info("Validating customer data...")

        issues = []

        # Check for required columns
        required_cols = ['customer_id', 'registration_date']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            issues.append(f"Missing required columns: {missing_cols}")

        # Check for duplicates
        if 'customer_id' in df.columns:
            duplicates = df['customer_id'].duplicated().sum()
            if duplicates > 0:
                issues.append(f"Found {duplicates} duplicate customer IDs")

        # Validate age range
        if 'age' in df.columns:
            invalid_ages = ((df['age'] < 0) | (df['age'] > 120)).sum()
            if invalid_ages > 0:
                issues.append(f"Found {invalid_ages} records with invalid age")

        if issues:
            logger.warning(f"Data validation issues: {issues}")
            return False, issues
        else:
            logger.info("Customer data validation passed!")
            return True, []


class DataExtractor:
    """
    Handles data extraction from various sources
    """

    def __init__(self, data_dir='../data'):
        self.data_dir = data_dir

    def extract_sales_data(self):
        """Extract sales data from CSV"""
        logger.info("Extracting sales data...")
        try:
            file_path = os.path.join(self.data_dir, 'sales_data.csv')
            df = pd.read_csv(file_path)
            logger.info(f"Successfully extracted {len(df):,} sales records")
            return df
        except Exception as e:
            logger.error(f"Error extracting sales data: {e}")
            raise

    def extract_customer_data(self):
        """Extract customer data from CSV"""
        logger.info("Extracting customer data...")
        try:
            file_path = os.path.join(self.data_dir, 'customer_data.csv')
            df = pd.read_csv(file_path)
            logger.info(f"Successfully extracted {len(df):,} customer records")
            return df
        except Exception as e:
            logger.error(f"Error extracting customer data: {e}")
            raise


class DataTransformer:
    """
    Handles data transformation and enrichment
    """

    @staticmethod
    def transform_sales_data(df):
        """Transform and clean sales data"""
        logger.info("Transforming sales data...")

        df = df.copy()

        # Convert date columns
        df['transaction_date'] = pd.to_datetime(df['transaction_date'])

        # Extract date components
        df['year'] = df['transaction_date'].dt.year
        df['month'] = df['transaction_date'].dt.month
        df['day'] = df['transaction_date'].dt.day
        df['day_of_week'] = df['transaction_date'].dt.day_name()
        df['quarter'] = df['transaction_date'].dt.quarter
        df['week_of_year'] = df['transaction_date'].dt.isocalendar().week

        # Add time-based flags
        df['is_weekend'] = df['transaction_date'].dt.dayofweek.isin([5, 6])

        # Calculate profit margin (example: assume 30% margin)
        df['profit'] = df['revenue'] * 0.30

        # Categorize transaction value
        df['transaction_category'] = pd.cut(
            df['revenue'],
            bins=[0, 100, 500, 5000, 50000],
            labels=['Small', 'Medium', 'Large', 'Very Large']
        )

        logger.info(f"Transformed {len(df):,} sales records")
        logger.info(f"Date range: {df['transaction_date'].min()} to {df['transaction_date'].max()}")

        return df

    @staticmethod
    def transform_customer_data(df):
        """Transform and clean customer data"""
        logger.info("Transforming customer data...")

        df = df.copy()

        # Convert date columns
        df['registration_date'] = pd.to_datetime(df['registration_date'])

        # Calculate customer tenure (days since registration)
        df['customer_tenure_days'] = (datetime.now() - df['registration_date']).dt.days
        df['customer_tenure_years'] = df['customer_tenure_days'] / 365.25

        # Categorize customers by age
        df['age_group'] = pd.cut(
            df['age'],
            bins=[0, 25, 35, 45, 55, 100],
            labels=['18-25', '26-35', '36-45', '46-55', '55+']
        )

        # Clean text fields
        df['city'] = df['city'].str.strip().str.title()

        logger.info(f"Transformed {len(df):,} customer records")

        return df

    @staticmethod
    def create_customer_analytics(sales_df, customer_df):
        """Create enriched customer analytics dataset"""
        logger.info("Creating customer analytics dataset...")

        # Calculate customer metrics
        customer_metrics = sales_df.groupby('customer_id').agg({
            'transaction_id': 'nunique',
            'revenue': ['sum', 'mean', 'count'],
            'transaction_date': ['min', 'max']
        }).reset_index()

        customer_metrics.columns = [
            'customer_id',
            'total_transactions',
            'total_revenue',
            'avg_transaction_value',
            'transaction_count',
            'first_purchase_date',
            'last_purchase_date'
        ]

        # Calculate recency
        analysis_date = sales_df['transaction_date'].max()
        customer_metrics['days_since_last_purchase'] = \
            (analysis_date - customer_metrics['last_purchase_date']).dt.days

        # Calculate customer lifetime (days between first and last purchase)
        customer_metrics['customer_lifespan_days'] = \
            (customer_metrics['last_purchase_date'] - customer_metrics['first_purchase_date']).dt.days

        # Merge with customer demographic data
        customer_analytics = customer_metrics.merge(
            customer_df,
            on='customer_id',
            how='left'
        )

        # Calculate average days between purchases
        customer_analytics['avg_days_between_purchases'] = \
            customer_analytics['customer_lifespan_days'] / customer_analytics['total_transactions'].replace(0, 1)

        logger.info(f"Created analytics for {len(customer_analytics):,} customers")

        return customer_analytics

    @staticmethod
    def create_product_analytics(sales_df):
        """Create product performance analytics"""
        logger.info("Creating product analytics dataset...")

        product_analytics = sales_df.groupby(['product_category', 'product_name']).agg({
            'transaction_id': 'nunique',
            'quantity': 'sum',
            'revenue': ['sum', 'mean'],
            'customer_id': 'nunique'
        }).reset_index()

        product_analytics.columns = [
            'product_category',
            'product_name',
            'times_purchased',
            'total_units_sold',
            'total_revenue',
            'avg_transaction_value',
            'unique_customers'
        ]

        # Calculate revenue rank
        product_analytics['revenue_rank'] = \
            product_analytics['total_revenue'].rank(ascending=False)

        # Calculate revenue share
        product_analytics['revenue_share_pct'] = \
            (product_analytics['total_revenue'] / product_analytics['total_revenue'].sum() * 100)

        logger.info(f"Created analytics for {len(product_analytics):,} products")

        return product_analytics


class DataLoader:
    """
    Handles loading transformed data to target destinations
    """

    def __init__(self, output_dir='../data/processed'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def load_to_csv(self, df, filename):
        """Load dataframe to CSV file"""
        logger.info(f"Loading data to {filename}...")
        try:
            file_path = os.path.join(self.output_dir, filename)
            df.to_csv(file_path, index=False)
            logger.info(f"Successfully saved {len(df):,} records to {file_path}")
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")
            raise

    def load_summary_report(self, sales_df, customer_df, customer_analytics_df, product_analytics_df):
        """Generate and save summary report"""
        logger.info("Generating summary report...")

        report_path = os.path.join(self.output_dir, 'etl_summary_report.txt')

        with open(report_path, 'w') as f:
            f.write("="*70 + "\n")
            f.write("ETL PIPELINE SUMMARY REPORT\n")
            f.write("="*70 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("\n")

            f.write("1. DATA EXTRACTION\n")
            f.write("-" * 70 + "\n")
            f.write(f"Sales Records Extracted:    {len(sales_df):,}\n")
            f.write(f"Customer Records Extracted: {len(customer_df):,}\n")
            f.write("\n")

            f.write("2. DATA TRANSFORMATION\n")
            f.write("-" * 70 + "\n")
            f.write(f"Customer Analytics Created: {len(customer_analytics_df):,} records\n")
            f.write(f"Product Analytics Created:  {len(product_analytics_df):,} records\n")
            f.write("\n")

            f.write("3. KEY METRICS\n")
            f.write("-" * 70 + "\n")
            f.write(f"Total Revenue:              ${sales_df['revenue'].sum():,.2f}\n")
            f.write(f"Avg Transaction Value:      ${sales_df['revenue'].mean():,.2f}\n")
            f.write(f"Unique Customers:           {sales_df['customer_id'].nunique():,}\n")
            f.write(f"Date Range:                 {sales_df['transaction_date'].min()} to {sales_df['transaction_date'].max()}\n")
            f.write("\n")

            f.write("4. DATA QUALITY\n")
            f.write("-" * 70 + "\n")
            f.write(f"Sales Data Completeness:    {(1 - sales_df.isnull().sum().sum() / sales_df.size) * 100:.2f}%\n")
            f.write(f"Customer Data Completeness: {(1 - customer_df.isnull().sum().sum() / customer_df.size) * 100:.2f}%\n")
            f.write("\n")

            f.write("5. OUTPUT FILES\n")
            f.write("-" * 70 + "\n")
            f.write("- sales_transformed.csv\n")
            f.write("- customer_transformed.csv\n")
            f.write("- customer_analytics.csv\n")
            f.write("- product_analytics.csv\n")
            f.write("- etl_summary_report.txt\n")
            f.write("="*70 + "\n")

        logger.info(f"Summary report saved to {report_path}")


def run_etl_pipeline():
    """
    Main ETL pipeline execution
    """
    logger.info("="*70)
    logger.info("STARTING ETL PIPELINE")
    logger.info("="*70)

    start_time = datetime.now()

    try:
        # EXTRACT
        logger.info("\n[STEP 1] EXTRACTION")
        extractor = DataExtractor()
        sales_df = extractor.extract_sales_data()
        customer_df = extractor.extract_customer_data()

        # VALIDATE
        logger.info("\n[STEP 2] VALIDATION")
        validator = DataValidator()
        sales_valid, sales_issues = validator.validate_sales_data(sales_df)
        customer_valid, customer_issues = validator.validate_customer_data(customer_df)

        if not sales_valid or not customer_valid:
            logger.warning("Data validation found issues, but continuing with pipeline...")

        # TRANSFORM
        logger.info("\n[STEP 3] TRANSFORMATION")
        transformer = DataTransformer()
        sales_transformed = transformer.transform_sales_data(sales_df)
        customer_transformed = transformer.transform_customer_data(customer_df)
        customer_analytics = transformer.create_customer_analytics(sales_transformed, customer_transformed)
        product_analytics = transformer.create_product_analytics(sales_transformed)

        # LOAD
        logger.info("\n[STEP 4] LOADING")
        loader = DataLoader()
        loader.load_to_csv(sales_transformed, 'sales_transformed.csv')
        loader.load_to_csv(customer_transformed, 'customer_transformed.csv')
        loader.load_to_csv(customer_analytics, 'customer_analytics.csv')
        loader.load_to_csv(product_analytics, 'product_analytics.csv')
        loader.load_summary_report(sales_transformed, customer_transformed,
                                   customer_analytics, product_analytics)

        # Complete
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        logger.info("\n" + "="*70)
        logger.info("ETL PIPELINE COMPLETED SUCCESSFULLY")
        logger.info(f"Total execution time: {duration:.2f} seconds")
        logger.info("="*70)

        return True

    except Exception as e:
        logger.error(f"ETL Pipeline failed: {e}")
        raise


if __name__ == '__main__':
    run_etl_pipeline()
