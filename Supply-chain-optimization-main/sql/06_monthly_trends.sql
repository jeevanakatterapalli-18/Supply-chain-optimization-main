-- ============================================================
-- Business Question: How have shipment volume, revenue, and
-- delay rate trended month over month across 2023-2025?
--
-- Approach: Aggregate to Year/Month grain, then use LAG() to
-- compute month-over-month change without a self-join.
-- ============================================================

USE supply_chain_db;

WITH monthly AS (
    SELECT
        Year,
        Month,
        COUNT(*) AS shipment_count,
        SUM(Revenue_USD) AS total_revenue,
        ROUND(100.0 * SUM(CASE WHEN Shipment_Status = 'Delayed' THEN 1 ELSE 0 END) / COUNT(*), 2) AS delayed_pct
    FROM supply_chain
    GROUP BY Year, Month
)
SELECT
    Year,
    Month,
    shipment_count,
    total_revenue,
    delayed_pct,
    total_revenue - LAG(total_revenue) OVER (ORDER BY Year, Month) AS revenue_change_vs_prev_month,
    ROUND(
        100.0 * (total_revenue - LAG(total_revenue) OVER (ORDER BY Year, Month))
        / LAG(total_revenue) OVER (ORDER BY Year, Month), 2
    ) AS revenue_change_pct
FROM monthly
ORDER BY Year, Month;

-- Insight: revenue and delay rate both oscillate in a tight band across
-- all 36 months (~5,200-5,800 shipments/month, ~14.5-16.7% delayed, no
-- upward/downward trend or seasonality) — this is a flat baseline period,
-- not a business in growth/decline, and month-over-month swings (occasionally
-- +/-10%) are noise rather than a signal to act on.
