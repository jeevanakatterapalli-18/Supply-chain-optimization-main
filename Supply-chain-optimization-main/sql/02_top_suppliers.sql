-- ============================================================
-- Business Question: Who are our best and worst suppliers, and
-- how should we rank them for a supplier scorecard?
--
-- Approach: Aggregate per Supplier_ID (revenue, product count,
-- average rating, average performance score, on-time delivery
-- rate), then rank suppliers with a window function (RANK) so
-- ties are handled and we can pull "top N" without a LIMIT-only
-- approach that breaks on ties.
-- ============================================================

USE supply_chain_db;

WITH supplier_agg AS (
    SELECT
        Supplier_ID,
        COUNT(*)                          AS products_supplied,
        SUM(Revenue_USD)                  AS total_revenue,
        ROUND(AVG(Supplier_Rating), 2)    AS avg_rating,
        ROUND(AVG(Supplier_Performance_Score), 2) AS avg_performance_score,
        ROUND(AVG(On_Time_Delivery_Rate), 2)      AS avg_on_time_rate,
        SUM(CASE WHEN Shipment_Status = 'Delayed' THEN 1 ELSE 0 END) AS delayed_count
    FROM supply_chain
    GROUP BY Supplier_ID
)
SELECT
    Supplier_ID,
    products_supplied,
    total_revenue,
    avg_rating,
    avg_performance_score,
    avg_on_time_rate,
    delayed_count,
    RANK() OVER (ORDER BY total_revenue DESC) AS revenue_rank,
    RANK() OVER (ORDER BY avg_performance_score DESC) AS performance_rank
FROM supplier_agg
ORDER BY total_revenue DESC
LIMIT 10;

-- Insight: top supplier by revenue (SUP1168, $16.77M across 58 products)
-- ranks only 3,237th out of ~5,000 on performance score — revenue leadership
-- and performance leadership are two different scorecards here, and a
-- supplier scorecard should report both rather than picking one.

-- ------------------------------------------------------------
-- Same idea, flipped: worst-performing suppliers by performance
-- score, restricted to suppliers with a meaningful sample size
-- (>= 20 products) so a single unlucky product doesn't distort
-- the ranking.
-- ------------------------------------------------------------
WITH supplier_agg AS (
    SELECT
        Supplier_ID,
        COUNT(*) AS products_supplied,
        ROUND(AVG(Supplier_Performance_Score), 2) AS avg_performance_score,
        ROUND(AVG(On_Time_Delivery_Rate), 2) AS avg_on_time_rate,
        ROUND(AVG(Supply_Disruption_Risk), 2) AS avg_disruption_risk
    FROM supply_chain
    GROUP BY Supplier_ID
    HAVING COUNT(*) >= 20
)
SELECT *
FROM supplier_agg
ORDER BY avg_performance_score ASC
LIMIT 10;

-- Insight: the 10 weakest suppliers by performance score cluster in the
-- 34-37 range (vs. a ~50 dataset average), flagging a concrete supplier
-- review shortlist rather than "somewhere in the tail".
