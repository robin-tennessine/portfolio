# ETL Pipeline

This folder contains a production-ready ETL (Extract, Transform, Load) pipeline for processing retail sales data.

## Overview

The pipeline demonstrates end-to-end data processing skills including:
- Data extraction from multiple sources
- Data quality validation
- Complex transformations and feature engineering
- Analytics dataset creation
- Automated logging and error handling

## Pipeline Architecture

```
┌─────────────────┐
│    EXTRACT      │
│  - Sales Data   │
│  - Customer Data│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    VALIDATE     │
│  - Null checks  │
│  - Duplicates   │
│  - Data types   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   TRANSFORM     │
│  - Date parsing │
│  - Feature eng. │
│  - Aggregations │
│  - Enrichment   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│      LOAD       │
│  - CSV export   │
│  - Reports      │
│  - Logs         │
└─────────────────┘
```

## Features

### 1. Data Extraction
- CSV file reading
- Error handling and logging
- Configurable data sources

### 2. Data Validation
- Null value detection
- Duplicate record identification
- Business rule validation
- Data type verification

### 3. Data Transformation
- Date/time feature extraction (year, month, quarter, week, day of week)
- Customer analytics (RFM metrics, tenure, lifetime value)
- Product analytics (sales velocity, revenue ranking)
- Feature engineering (weekend flag, transaction categories)

### 4. Data Loading
- Analytics-ready CSV outputs
- Automated summary reports
- Comprehensive logging

## How to Run

```bash
# Ensure you have generated sample data first
cd ../data
python generate_sample_data.py

# Run the ETL pipeline
cd ../etl_pipeline
python data_pipeline.py
```

## Output Files

The pipeline creates the following files in `../data/processed/`:

1. **sales_transformed.csv** - Enhanced sales data with date features
2. **customer_transformed.csv** - Enriched customer demographic data
3. **customer_analytics.csv** - Customer behavior metrics (RFM, tenure, etc.)
4. **product_analytics.csv** - Product performance metrics
5. **etl_summary_report.txt** - Pipeline execution summary
6. **etl_pipeline.log** - Detailed execution logs

## Code Structure

### Classes

**DataExtractor**
- Handles data extraction from various sources
- Supports CSV, could be extended for databases, APIs

**DataValidator**
- Validates data quality and integrity
- Implements business rules
- Reports data quality issues

**DataTransformer**
- Cleans and transforms raw data
- Creates derived features
- Builds analytics datasets

**DataLoader**
- Exports processed data to target destinations
- Generates summary reports
- Handles file I/O operations

## Key Transformations

### Sales Data Enrichment
- Extract date components (year, month, day, quarter, week)
- Weekend/weekday flag
- Transaction size categorization
- Profit margin calculation

### Customer Analytics
- Total transactions and revenue per customer
- Average transaction value
- Recency (days since last purchase)
- Customer tenure
- Average days between purchases

### Product Analytics
- Revenue and unit sales by product
- Revenue ranking and share
- Unique customer count
- Purchase frequency

## Skills Demonstrated

- **Python Programming**: Object-oriented design, error handling
- **Data Processing**: pandas, numpy for data manipulation
- **ETL Best Practices**: Modular code, logging, validation
- **Data Quality**: Comprehensive validation checks
- **Feature Engineering**: Creating analytical features from raw data
- **Documentation**: Clear code comments and documentation

## Extending the Pipeline

This pipeline can be extended to:
- Connect to databases (PostgreSQL, MySQL)
- Integrate with cloud storage (S3, Azure Blob)
- Add more data sources
- Implement incremental loading
- Add data quality alerts
- Schedule automated runs
- Export to data warehouses

## Dependencies

```
pandas
numpy
```

See `../requirements.txt` for complete dependencies.

## Logs

Pipeline execution is logged to:
- Console output (stdout)
- `etl_pipeline.log` file

Log levels include INFO, WARNING, and ERROR messages for debugging and monitoring.
