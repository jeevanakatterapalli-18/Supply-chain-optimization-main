-- ============================================================
-- Business Question: Smooth out month-to-month noise in revenue
-- and shipping cost to see the underlying trend line.
--
-- Approach: Aggregate to monthly grain in a CTE, then apply a
-- 3-month moving average with AVG() OVER (... ROWS BETWEEN 2
-- PRECEDING AND CURRENT ROW).
-- ============================================================

USE supply_chain_db;

WITH monthly AS (
    SELECT
        Year,
        Month,
        SUM(Revenue_USD) AS total_revenue,
        ROUND(AVG(Shipping_Cost_USD), 2) AS avg_shipping_cost
    FROM supply_chain
    GROUP BY Year, Month
)
SELECT
    Year,
    Month,
    total_revenue,
    ROUND(AVG(total_revenue) OVER (
        ORDER BY Year, Month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS revenue_3mo_moving_avg,
    avg_shipping_cost,
    ROUND(AVG(avg_shipping_cost) OVER (
        ORDER BY Year, Month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS shipping_cost_3mo_moving_avg
FROM monthly
ORDER BY Year, Month;

-- Insight: the 3-month moving average stays inside a narrow ~$1.35B-$1.42B
-- band for revenue and ~$247-$253 for shipping cost across the full
-- 3-year window — confirms (per 06_monthly_trends.sql) that raw
-- month-to-month swings are noise around a flat baseline, not a
-- masked trend the smoothing reveals.
