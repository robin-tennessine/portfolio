-- ============================================
-- CUSTOMER BEHAVIOR & INSIGHTS ANALYSIS
-- ============================================
-- Advanced SQL queries for understanding customer patterns
-- and driving business decisions
-- ============================================

-- 1. CUSTOMER LIFETIME VALUE ANALYSIS
-- Calculate actual LTV based on transactions and compare with estimated
SELECT
    c.customer_id,
    c.customer_segment,
    c.registration_date,
    c.lifetime_value as estimated_ltv,
    COUNT(s.transaction_id) as total_purchases,
    SUM(s.revenue) as actual_revenue,
    ROUND(AVG(s.revenue), 2) as avg_purchase_value,
    MAX(s.transaction_date) as last_purchase_date,
    ROUND(actual_revenue - c.lifetime_value, 2) as ltv_variance
FROM customer_data c
LEFT JOIN sales_data s ON c.customer_id = s.customer_id
GROUP BY c.customer_id, c.customer_segment, c.registration_date, c.lifetime_value
ORDER BY actual_revenue DESC
LIMIT 20;


-- 2. RFM ANALYSIS (Recency, Frequency, Monetary)
-- Segment customers based on purchase behavior
WITH rfm_calc AS (
    SELECT
        customer_id,
        CURRENT_DATE - MAX(transaction_date)::DATE as recency_days,
        COUNT(transaction_id) as frequency,
        SUM(revenue) as monetary
    FROM sales_data
    GROUP BY customer_id
),
rfm_scores AS (
    SELECT
        customer_id,
        recency_days,
        frequency,
        monetary,
        NTILE(5) OVER (ORDER BY recency_days DESC) as r_score,
        NTILE(5) OVER (ORDER BY frequency ASC) as f_score,
        NTILE(5) OVER (ORDER BY monetary ASC) as m_score
    FROM rfm_calc
)
SELECT
    customer_id,
    recency_days,
    frequency,
    ROUND(monetary, 2) as monetary_value,
    r_score,
    f_score,
    m_score,
    (r_score + f_score + m_score) as rfm_total_score,
    CASE
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
        WHEN r_score >= 3 AND f_score >= 3 THEN 'Loyal Customers'
        WHEN r_score >= 4 THEN 'Recent Customers'
        WHEN f_score >= 4 THEN 'Frequent Buyers'
        WHEN m_score >= 4 THEN 'High Spenders'
        WHEN r_score <= 2 AND f_score <= 2 THEN 'At Risk'
        WHEN r_score <= 2 THEN 'Lost Customers'
        ELSE 'Potential Loyalists'
    END as customer_segment_rfm
FROM rfm_scores
ORDER BY rfm_total_score DESC;


-- 3. CUSTOMER RETENTION ANALYSIS
-- Track month-over-month customer retention
WITH monthly_customers AS (
    SELECT
        DATE_TRUNC('month', transaction_date) as month,
        customer_id
    FROM sales_data
    GROUP BY DATE_TRUNC('month', transaction_date), customer_id
),
retention AS (
    SELECT
        curr.month as current_month,
        COUNT(DISTINCT curr.customer_id) as current_customers,
        COUNT(DISTINCT prev.customer_id) as retained_customers,
        ROUND(
            COUNT(DISTINCT prev.customer_id) * 100.0 /
            COUNT(DISTINCT curr.customer_id), 2
        ) as retention_rate
    FROM monthly_customers curr
    LEFT JOIN monthly_customers prev
        ON curr.customer_id = prev.customer_id
        AND prev.month = curr.month - INTERVAL '1 month'
    GROUP BY curr.month
)
SELECT
    current_month,
    current_customers,
    retained_customers,
    retention_rate
FROM retention
ORDER BY current_month DESC;


-- 4. CUSTOMER CHURN ANALYSIS
-- Identify customers who haven't purchased recently
WITH last_purchase AS (
    SELECT
        customer_id,
        MAX(transaction_date) as last_purchase_date,
        COUNT(transaction_id) as total_purchases,
        SUM(revenue) as total_spent
    FROM sales_data
    GROUP BY customer_id
)
SELECT
    c.customer_id,
    c.customer_segment,
    c.city,
    lp.last_purchase_date,
    CURRENT_DATE - lp.last_purchase_date::DATE as days_since_purchase,
    lp.total_purchases,
    ROUND(lp.total_spent, 2) as total_spent,
    CASE
        WHEN CURRENT_DATE - lp.last_purchase_date::DATE > 180 THEN 'High Risk'
        WHEN CURRENT_DATE - lp.last_purchase_date::DATE > 90 THEN 'Medium Risk'
        WHEN CURRENT_DATE - lp.last_purchase_date::DATE > 60 THEN 'Low Risk'
        ELSE 'Active'
    END as churn_risk
FROM customer_data c
JOIN last_purchase lp ON c.customer_id = lp.customer_id
WHERE CURRENT_DATE - lp.last_purchase_date::DATE > 60
ORDER BY days_since_purchase DESC;


-- 5. CUSTOMER ACQUISITION BY CHANNEL/CITY
-- Analyze customer distribution and performance by location
SELECT
    city,
    customer_segment,
    COUNT(DISTINCT c.customer_id) as customer_count,
    COALESCE(COUNT(DISTINCT s.transaction_id), 0) as total_transactions,
    COALESCE(SUM(s.revenue), 0) as total_revenue,
    ROUND(COALESCE(AVG(s.revenue), 0), 2) as avg_transaction_value,
    ROUND(
        COALESCE(SUM(s.revenue), 0) / COUNT(DISTINCT c.customer_id), 2
    ) as revenue_per_customer
FROM customer_data c
LEFT JOIN sales_data s ON c.customer_id = s.customer_id
GROUP BY city, customer_segment
ORDER BY total_revenue DESC;


-- 6. PURCHASE FREQUENCY DISTRIBUTION
-- Understand how often customers make purchases
WITH purchase_counts AS (
    SELECT
        customer_id,
        COUNT(transaction_id) as purchase_count,
        SUM(revenue) as total_spent
    FROM sales_data
    GROUP BY customer_id
)
SELECT
    CASE
        WHEN purchase_count = 1 THEN '1 purchase'
        WHEN purchase_count BETWEEN 2 AND 5 THEN '2-5 purchases'
        WHEN purchase_count BETWEEN 6 AND 10 THEN '6-10 purchases'
        WHEN purchase_count BETWEEN 11 AND 20 THEN '11-20 purchases'
        ELSE '20+ purchases'
    END as purchase_frequency,
    COUNT(customer_id) as customer_count,
    ROUND(AVG(total_spent), 2) as avg_total_spent,
    ROUND(SUM(total_spent), 2) as total_revenue
FROM purchase_counts
GROUP BY
    CASE
        WHEN purchase_count = 1 THEN '1 purchase'
        WHEN purchase_count BETWEEN 2 AND 5 THEN '2-5 purchases'
        WHEN purchase_count BETWEEN 6 AND 10 THEN '6-10 purchases'
        WHEN purchase_count BETWEEN 11 AND 20 THEN '11-20 purchases'
        ELSE '20+ purchases'
    END
ORDER BY MIN(purchase_count);


-- 7. CROSS-SELLING ANALYSIS
-- Identify products frequently purchased together
WITH product_pairs AS (
    SELECT
        s1.transaction_id,
        s1.product_name as product_a,
        s2.product_name as product_b
    FROM sales_data s1
    JOIN sales_data s2
        ON s1.transaction_id = s2.transaction_id
        AND s1.product_name < s2.product_name  -- Avoid duplicates
)
SELECT
    product_a,
    product_b,
    COUNT(*) as times_purchased_together,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(DISTINCT transaction_id) FROM sales_data), 2
    ) as pct_of_transactions
FROM product_pairs
GROUP BY product_a, product_b
HAVING COUNT(*) > 5
ORDER BY times_purchased_together DESC
LIMIT 15;


-- 8. CUSTOMER DEMOGRAPHICS ANALYSIS
-- Revenue performance by demographic segments
SELECT
    CASE
        WHEN age < 25 THEN '18-24'
        WHEN age BETWEEN 25 AND 34 THEN '25-34'
        WHEN age BETWEEN 35 AND 44 THEN '35-44'
        WHEN age BETWEEN 45 AND 54 THEN '45-54'
        ELSE '55+'
    END as age_group,
    gender,
    COUNT(DISTINCT c.customer_id) as customer_count,
    COUNT(s.transaction_id) as total_transactions,
    ROUND(SUM(s.revenue), 2) as total_revenue,
    ROUND(AVG(s.revenue), 2) as avg_transaction_value
FROM customer_data c
LEFT JOIN sales_data s ON c.customer_id = s.customer_id
GROUP BY age_group, gender
ORDER BY total_revenue DESC;


-- 9. NEW VS RETURNING CUSTOMERS MONTHLY
-- Track customer acquisition vs retention
WITH monthly_customer_type AS (
    SELECT
        DATE_TRUNC('month', s.transaction_date) as month,
        s.customer_id,
        MIN(s.transaction_date) OVER (PARTITION BY s.customer_id) as first_purchase,
        s.transaction_date
    FROM sales_data s
)
SELECT
    month,
    COUNT(DISTINCT CASE
        WHEN DATE_TRUNC('month', first_purchase) = month THEN customer_id
    END) as new_customers,
    COUNT(DISTINCT CASE
        WHEN DATE_TRUNC('month', first_purchase) < month THEN customer_id
    END) as returning_customers,
    COUNT(DISTINCT customer_id) as total_active_customers
FROM monthly_customer_type
GROUP BY month
ORDER BY month DESC;


-- 10. AVERAGE DAYS BETWEEN PURCHASES
-- Calculate purchase cycle for repeat customers
WITH purchase_dates AS (
    SELECT
        customer_id,
        transaction_date,
        LAG(transaction_date) OVER (
            PARTITION BY customer_id ORDER BY transaction_date
        ) as previous_purchase_date
    FROM sales_data
),
days_between AS (
    SELECT
        customer_id,
        transaction_date - previous_purchase_date as days_between_purchases
    FROM purchase_dates
    WHERE previous_purchase_date IS NOT NULL
)
SELECT
    c.customer_segment,
    COUNT(DISTINCT db.customer_id) as repeat_customers,
    ROUND(AVG(days_between_purchases), 1) as avg_days_between_purchases,
    ROUND(MIN(days_between_purchases), 1) as min_days,
    ROUND(MAX(days_between_purchases), 1) as max_days
FROM days_between db
JOIN customer_data c ON db.customer_id = c.customer_id
GROUP BY c.customer_segment
ORDER BY avg_days_between_purchases;
