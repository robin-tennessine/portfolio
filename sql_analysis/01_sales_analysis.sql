-- ============================================
-- SALES PERFORMANCE ANALYSIS
-- ============================================
-- This script demonstrates SQL skills for sales analytics
-- including aggregations, window functions, and CTEs
-- ============================================

-- 1. OVERALL SALES PERFORMANCE
-- Calculate total revenue, transactions, and average order value
SELECT
    COUNT(DISTINCT transaction_id) as total_transactions,
    COUNT(DISTINCT customer_id) as unique_customers,
    SUM(revenue) as total_revenue,
    AVG(revenue) as avg_transaction_value,
    MIN(transaction_date) as first_transaction,
    MAX(transaction_date) as last_transaction
FROM sales_data;


-- 2. MONTHLY SALES TREND
-- Analyze sales performance over time with month-over-month growth
WITH monthly_sales AS (
    SELECT
        DATE_TRUNC('month', transaction_date) as month,
        SUM(revenue) as monthly_revenue,
        COUNT(DISTINCT transaction_id) as transaction_count,
        COUNT(DISTINCT customer_id) as active_customers
    FROM sales_data
    GROUP BY DATE_TRUNC('month', transaction_date)
),
sales_with_growth AS (
    SELECT
        month,
        monthly_revenue,
        transaction_count,
        active_customers,
        LAG(monthly_revenue) OVER (ORDER BY month) as prev_month_revenue,
        monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY month) as revenue_change
    FROM monthly_sales
)
SELECT
    month,
    monthly_revenue,
    transaction_count,
    active_customers,
    prev_month_revenue,
    revenue_change,
    ROUND((revenue_change / NULLIF(prev_month_revenue, 0) * 100), 2) as pct_change
FROM sales_with_growth
ORDER BY month DESC;


-- 3. PRODUCT CATEGORY PERFORMANCE
-- Compare revenue and transaction metrics across product categories
SELECT
    product_category,
    COUNT(transaction_id) as total_transactions,
    SUM(quantity) as total_units_sold,
    SUM(revenue) as total_revenue,
    ROUND(AVG(revenue), 2) as avg_transaction_value,
    ROUND(SUM(revenue) * 100.0 / SUM(SUM(revenue)) OVER (), 2) as revenue_share_pct
FROM sales_data
GROUP BY product_category
ORDER BY total_revenue DESC;


-- 4. TOP SELLING PRODUCTS
-- Identify best performing products by revenue and volume
SELECT
    product_name,
    product_category,
    COUNT(transaction_id) as times_purchased,
    SUM(quantity) as total_quantity_sold,
    SUM(revenue) as total_revenue,
    ROUND(AVG(unit_price), 2) as avg_unit_price
FROM sales_data
GROUP BY product_name, product_category
ORDER BY total_revenue DESC
LIMIT 10;


-- 5. STORE LOCATION PERFORMANCE
-- Compare sales performance across different store locations
SELECT
    store_location,
    COUNT(DISTINCT transaction_id) as total_transactions,
    COUNT(DISTINCT customer_id) as unique_customers,
    SUM(revenue) as total_revenue,
    ROUND(AVG(revenue), 2) as avg_transaction_value,
    ROUND(SUM(revenue) * 100.0 / SUM(SUM(revenue)) OVER (), 2) as revenue_contribution_pct
FROM sales_data
GROUP BY store_location
ORDER BY total_revenue DESC;


-- 6. DAY OF WEEK ANALYSIS
-- Identify peak sales days to optimize staffing and inventory
SELECT
    TO_CHAR(transaction_date, 'Day') as day_of_week,
    EXTRACT(DOW FROM transaction_date) as day_number,
    COUNT(transaction_id) as transaction_count,
    SUM(revenue) as total_revenue,
    ROUND(AVG(revenue), 2) as avg_transaction_value,
    COUNT(DISTINCT customer_id) as unique_customers
FROM sales_data
GROUP BY day_of_week, day_number
ORDER BY day_number;


-- 7. HOURLY SALES PATTERN (if time data available)
-- Identify peak hours for business optimization
SELECT
    EXTRACT(HOUR FROM transaction_date) as hour_of_day,
    COUNT(transaction_id) as transaction_count,
    SUM(revenue) as total_revenue,
    ROUND(AVG(revenue), 2) as avg_transaction_value
FROM sales_data
GROUP BY EXTRACT(HOUR FROM transaction_date)
ORDER BY hour_of_day;


-- 8. SALES PERFORMANCE BY CUSTOMER SEGMENT
-- Compare how different customer segments contribute to sales
SELECT
    c.customer_segment,
    COUNT(DISTINCT s.transaction_id) as total_transactions,
    COUNT(DISTINCT s.customer_id) as customer_count,
    SUM(s.revenue) as total_revenue,
    ROUND(AVG(s.revenue), 2) as avg_transaction_value,
    ROUND(SUM(s.revenue) / COUNT(DISTINCT s.customer_id), 2) as revenue_per_customer
FROM sales_data s
JOIN customer_data c ON s.customer_id = c.customer_id
GROUP BY c.customer_segment
ORDER BY total_revenue DESC;


-- 9. COHORT ANALYSIS - First Purchase Month
-- Track customer behavior based on acquisition month
WITH first_purchase AS (
    SELECT
        customer_id,
        DATE_TRUNC('month', MIN(transaction_date)) as cohort_month
    FROM sales_data
    GROUP BY customer_id
),
cohort_sales AS (
    SELECT
        fp.cohort_month,
        DATE_TRUNC('month', s.transaction_date) as transaction_month,
        COUNT(DISTINCT s.customer_id) as active_customers,
        SUM(s.revenue) as cohort_revenue
    FROM sales_data s
    JOIN first_purchase fp ON s.customer_id = fp.customer_id
    GROUP BY fp.cohort_month, DATE_TRUNC('month', s.transaction_date)
)
SELECT
    cohort_month,
    transaction_month,
    active_customers,
    cohort_revenue,
    ROUND(cohort_revenue / active_customers, 2) as revenue_per_customer
FROM cohort_sales
ORDER BY cohort_month, transaction_month;


-- 10. CUMULATIVE REVENUE (Running Total)
-- Calculate cumulative revenue over time
SELECT
    DATE(transaction_date) as transaction_date,
    SUM(revenue) as daily_revenue,
    SUM(SUM(revenue)) OVER (ORDER BY DATE(transaction_date)) as cumulative_revenue
FROM sales_data
GROUP BY DATE(transaction_date)
ORDER BY transaction_date;
