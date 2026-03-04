-- ============================================
-- PRODUCT PERFORMANCE & INVENTORY INSIGHTS
-- ============================================
-- SQL queries for product analysis and optimization
-- ============================================

-- 1. PRODUCT PERFORMANCE OVERVIEW
-- Comprehensive product metrics
SELECT
    product_name,
    product_category,
    COUNT(DISTINCT transaction_id) as times_sold,
    SUM(quantity) as total_units_sold,
    SUM(revenue) as total_revenue,
    ROUND(AVG(unit_price), 2) as avg_price,
    ROUND(SUM(revenue) / SUM(quantity), 2) as revenue_per_unit,
    COUNT(DISTINCT customer_id) as unique_customers
FROM sales_data
GROUP BY product_name, product_category
ORDER BY total_revenue DESC;


-- 2. PRODUCT GROWTH TREND
-- Month-over-month product performance
WITH monthly_product_sales AS (
    SELECT
        DATE_TRUNC('month', transaction_date) as month,
        product_category,
        SUM(revenue) as monthly_revenue,
        SUM(quantity) as units_sold
    FROM sales_data
    GROUP BY DATE_TRUNC('month', transaction_date), product_category
),
product_growth AS (
    SELECT
        month,
        product_category,
        monthly_revenue,
        units_sold,
        LAG(monthly_revenue) OVER (
            PARTITION BY product_category ORDER BY month
        ) as prev_month_revenue
    FROM monthly_product_sales
)
SELECT
    month,
    product_category,
    monthly_revenue,
    units_sold,
    prev_month_revenue,
    monthly_revenue - prev_month_revenue as revenue_change,
    ROUND(
        ((monthly_revenue - prev_month_revenue) /
        NULLIF(prev_month_revenue, 0) * 100), 2
    ) as growth_rate_pct
FROM product_growth
WHERE prev_month_revenue IS NOT NULL
ORDER BY month DESC, monthly_revenue DESC;


-- 3. PRODUCT CATEGORY MIX ANALYSIS
-- Revenue contribution by category over time
SELECT
    DATE_TRUNC('month', transaction_date) as month,
    product_category,
    SUM(revenue) as category_revenue,
    ROUND(
        SUM(revenue) * 100.0 /
        SUM(SUM(revenue)) OVER (PARTITION BY DATE_TRUNC('month', transaction_date)),
        2
    ) as category_revenue_share_pct
FROM sales_data
GROUP BY DATE_TRUNC('month', transaction_date), product_category
ORDER BY month DESC, category_revenue DESC;


-- 4. FAST MOVING VS SLOW MOVING PRODUCTS
-- Classify products by sales velocity
WITH product_velocity AS (
    SELECT
        product_name,
        product_category,
        COUNT(transaction_id) as transaction_count,
        SUM(quantity) as total_quantity,
        SUM(revenue) as total_revenue,
        MAX(transaction_date) - MIN(transaction_date) as days_in_catalog,
        ROUND(
            SUM(quantity)::NUMERIC /
            NULLIF((MAX(transaction_date) - MIN(transaction_date)), 0),
            2
        ) as avg_daily_sales
    FROM sales_data
    GROUP BY product_name, product_category
)
SELECT
    product_name,
    product_category,
    transaction_count,
    total_quantity,
    total_revenue,
    days_in_catalog,
    avg_daily_sales,
    CASE
        WHEN avg_daily_sales >= 5 THEN 'Fast Moving'
        WHEN avg_daily_sales >= 2 THEN 'Medium Moving'
        WHEN avg_daily_sales >= 0.5 THEN 'Slow Moving'
        ELSE 'Very Slow Moving'
    END as velocity_category
FROM product_velocity
ORDER BY avg_daily_sales DESC;


-- 5. PRODUCT PROFITABILITY RANKING
-- Rank products by revenue and volume
SELECT
    product_name,
    product_category,
    SUM(revenue) as total_revenue,
    SUM(quantity) as total_units_sold,
    DENSE_RANK() OVER (ORDER BY SUM(revenue) DESC) as revenue_rank,
    DENSE_RANK() OVER (ORDER BY SUM(quantity) DESC) as volume_rank,
    ROUND(
        SUM(revenue) * 100.0 / SUM(SUM(revenue)) OVER (), 2
    ) as revenue_contribution_pct
FROM sales_data
GROUP BY product_name, product_category
ORDER BY total_revenue DESC;


-- 6. PARETO ANALYSIS (80/20 RULE)
-- Identify top 20% products generating 80% revenue
WITH product_revenue AS (
    SELECT
        product_name,
        SUM(revenue) as total_revenue
    FROM sales_data
    GROUP BY product_name
),
cumulative_revenue AS (
    SELECT
        product_name,
        total_revenue,
        SUM(total_revenue) OVER (ORDER BY total_revenue DESC) as cumulative_revenue,
        SUM(total_revenue) OVER () as grand_total
    FROM product_revenue
)
SELECT
    product_name,
    ROUND(total_revenue, 2) as total_revenue,
    ROUND(cumulative_revenue, 2) as cumulative_revenue,
    ROUND(cumulative_revenue * 100.0 / grand_total, 2) as cumulative_pct,
    CASE
        WHEN cumulative_revenue * 100.0 / grand_total <= 80 THEN 'Top 80%'
        ELSE 'Bottom 20%'
    END as pareto_category
FROM cumulative_revenue
ORDER BY total_revenue DESC;


-- 7. SEASONAL PRODUCT PERFORMANCE
-- Identify seasonal trends by product category
SELECT
    EXTRACT(MONTH FROM transaction_date) as month,
    TO_CHAR(transaction_date, 'Month') as month_name,
    product_category,
    COUNT(transaction_id) as transaction_count,
    SUM(quantity) as units_sold,
    ROUND(SUM(revenue), 2) as total_revenue
FROM sales_data
GROUP BY EXTRACT(MONTH FROM transaction_date), TO_CHAR(transaction_date, 'Month'), product_category
ORDER BY month, total_revenue DESC;


-- 8. PRODUCT AFFINITY BY CUSTOMER SEGMENT
-- Which products appeal to which customer segments
SELECT
    c.customer_segment,
    s.product_category,
    s.product_name,
    COUNT(s.transaction_id) as purchase_count,
    COUNT(DISTINCT s.customer_id) as unique_buyers,
    ROUND(SUM(s.revenue), 2) as total_revenue,
    ROUND(AVG(s.revenue), 2) as avg_transaction_value
FROM sales_data s
JOIN customer_data c ON s.customer_id = c.customer_id
GROUP BY c.customer_segment, s.product_category, s.product_name
ORDER BY c.customer_segment, total_revenue DESC;


-- 9. PRODUCT PERFORMANCE BY STORE LOCATION
-- Optimize inventory placement based on location performance
SELECT
    store_location,
    product_category,
    product_name,
    COUNT(transaction_id) as times_sold,
    SUM(quantity) as total_units,
    ROUND(SUM(revenue), 2) as total_revenue,
    ROUND(
        SUM(revenue) * 100.0 /
        SUM(SUM(revenue)) OVER (PARTITION BY store_location),
        2
    ) as revenue_share_pct
FROM sales_data
GROUP BY store_location, product_category, product_name
ORDER BY store_location, total_revenue DESC;


-- 10. PRODUCT CANNIBALIZATION ANALYSIS
-- Identify if new products are eating into existing product sales
WITH product_time_series AS (
    SELECT
        DATE_TRUNC('month', transaction_date) as month,
        product_name,
        SUM(revenue) as monthly_revenue
    FROM sales_data
    WHERE product_category = 'Smartphone'  -- Focus on smartphone category
    GROUP BY DATE_TRUNC('month', transaction_date), product_name
),
product_changes AS (
    SELECT
        month,
        product_name,
        monthly_revenue,
        LAG(monthly_revenue) OVER (
            PARTITION BY product_name ORDER BY month
        ) as prev_revenue
    FROM product_time_series
)
SELECT
    month,
    product_name,
    monthly_revenue,
    prev_revenue,
    COALESCE(monthly_revenue - prev_revenue, 0) as revenue_change,
    ROUND(
        COALESCE(
            (monthly_revenue - prev_revenue) * 100.0 /
            NULLIF(prev_revenue, 0), 0
        ), 2
    ) as pct_change
FROM product_changes
WHERE prev_revenue IS NOT NULL
ORDER BY month DESC, monthly_revenue DESC;


-- 11. PRODUCT BUNDLE OPPORTUNITIES
-- Find products commonly purchased in same transaction
SELECT
    s1.product_name as product_1,
    s2.product_name as product_2,
    COUNT(DISTINCT s1.transaction_id) as co_purchase_count,
    ROUND(AVG(s1.revenue + s2.revenue), 2) as avg_bundle_value
FROM sales_data s1
JOIN sales_data s2
    ON s1.transaction_id = s2.transaction_id
    AND s1.product_name < s2.product_name
GROUP BY s1.product_name, s2.product_name
HAVING COUNT(DISTINCT s1.transaction_id) >= 5
ORDER BY co_purchase_count DESC
LIMIT 20;


-- 12. PRICE SENSITIVITY ANALYSIS
-- Understand how price points affect sales volume
SELECT
    product_category,
    CASE
        WHEN unit_price < 100 THEN 'Under 100'
        WHEN unit_price BETWEEN 100 AND 500 THEN '100-500'
        WHEN unit_price BETWEEN 501 AND 5000 THEN '501-5000'
        WHEN unit_price BETWEEN 5001 AND 15000 THEN '5001-15000'
        ELSE '15000+'
    END as price_range,
    COUNT(transaction_id) as transaction_count,
    SUM(quantity) as units_sold,
    ROUND(SUM(revenue), 2) as total_revenue,
    ROUND(AVG(unit_price), 2) as avg_price
FROM sales_data
GROUP BY product_category, price_range
ORDER BY product_category, MIN(unit_price);
