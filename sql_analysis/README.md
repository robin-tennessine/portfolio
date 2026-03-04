# SQL Analysis Portfolio

This folder contains SQL queries demonstrating advanced analytical skills for business intelligence and data analysis.

## Files Overview

### 01_sales_analysis.sql
Comprehensive sales performance analytics including:
- Overall sales metrics (revenue, transactions, AOV)
- Monthly sales trends with MoM growth
- Product category performance
- Top selling products
- Store location comparison
- Day of week and hourly patterns
- Customer segment analysis
- Cohort analysis
- Running totals and cumulative metrics

**Key Skills Demonstrated:**
- Aggregations and GROUP BY
- Window functions (LAG, SUM OVER, NTILE)
- Common Table Expressions (CTEs)
- Date functions and time-series analysis
- Self-joins and subqueries

### 02_customer_insights.sql
Customer behavior and retention analytics:
- Customer Lifetime Value (LTV) analysis
- RFM (Recency, Frequency, Monetary) segmentation
- Retention and churn analysis
- Customer acquisition metrics
- Purchase frequency distribution
- Cross-selling opportunities
- Demographics analysis
- New vs returning customers
- Purchase cycle analysis

**Key Skills Demonstrated:**
- Advanced window functions (NTILE, RANK)
- Complex CASE statements for segmentation
- Multi-level CTEs
- Cohort analysis
- Self-joins for pattern detection

### 03_product_performance.sql
Product analytics and inventory optimization:
- Product performance metrics
- Growth trends and seasonality
- Category mix analysis
- Fast/slow moving product classification
- Pareto analysis (80/20 rule)
- Product affinity by customer segment
- Store-level product performance
- Cannibalization analysis
- Bundle opportunities
- Price sensitivity

**Key Skills Demonstrated:**
- Advanced window functions (DENSE_RANK, PARTITION BY)
- Cumulative calculations
- Time-series comparisons
- Statistical analysis
- Business rule implementation

## How to Use

These queries are designed to work with the sample data in the `/data` folder. You can:

1. **Run in your preferred SQL environment:**
   - PostgreSQL (recommended)
   - MySQL (may need minor syntax adjustments)
   - SQLite (some functions may not be available)

2. **Import sample data:**
   ```bash
   # First, generate the sample data
   cd ../data
   python generate_sample_data.py

   # Then import to your database
   # (specific commands depend on your DBMS)
   ```

3. **Execute queries:**
   - Run queries individually to see specific insights
   - Modify date ranges, filters, and parameters as needed
   - Use as templates for similar analyses

## Business Value

These analyses provide actionable insights for:
- **Sales Teams:** Identify top products, peak times, and growth opportunities
- **Marketing:** Customer segmentation, retention strategies, and targeting
- **Inventory Management:** Stock optimization based on velocity and location
- **Executive Dashboard:** KPIs, trends, and performance metrics

## Technical Notes

- All queries use standard SQL with PostgreSQL syntax
- Window functions and CTEs are heavily utilized
- Queries are optimized for readability and learning
- Comments explain business logic and calculations
- Can be adapted for different business contexts

## Contact

Questions about these analyses? Feel free to reach out!
