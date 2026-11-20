-- ============================================================
-- Business Question: Classic ABC inventory analysis — which
-- small share of products drives most of our revenue (A), which
-- are the mid-tier (B), and which are low-priority "long tail" (C)?
--
-- Approach: Rank products by revenue, compute a running/cumulative
-- revenue share with a window function, then bucket by the
-- standard 70/20/10 ABC thresholds.
-- ============================================================

USE supply_chain_db;

WITH ranked AS (
    SELECT
        Product_ID,
        Product_Category,
        Revenue_USD,
        SUM(Revenue_USD) OVER (ORDER BY Revenue_USD DESC
                                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_revenue,
        SUM(Revenue_USD) OVER () AS total_revenue
    FROM supply_chain
),
classified AS (
    SELECT
        Product_ID,
        Product_Category,
        Revenue_USD,
        ROUND(100.0 * running_revenue / total_revenue, 4) AS cumulative_revenue_pct,
        CASE
            WHEN running_revenue / total_revenue <= 0.70 THEN 'A'
            WHEN running_revenue / total_revenue <= 0.90 THEN 'B'
            ELSE 'C'
        END AS abc_class
    FROM ranked
)
SELECT
    abc_class,
    COUNT(*) AS product_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_of_products,
    ROUND(SUM(Revenue_USD), 2) AS class_revenue,
    ROUND(100.0 * SUM(Revenue_USD) / SUM(SUM(Revenue_USD)) OVER (), 2) AS pct_of_revenue
FROM classified
GROUP BY abc_class
ORDER BY abc_class;

-- Insight: Class A takes 45.3% of products (not the classic ~20%) to reach
-- 70% of revenue. Real retail revenue is typically Pareto-skewed (a small
-- SKU set dominates); here Revenue_USD is close to uniformly distributed
-- per product (see docs/data_dictionary.md), so ABC segmentation is far
-- less concentrated than textbook ABC analysis would suggest — worth
-- calling out explicitly rather than presenting a textbook 80/20 split
-- that this data doesn't actually show.
