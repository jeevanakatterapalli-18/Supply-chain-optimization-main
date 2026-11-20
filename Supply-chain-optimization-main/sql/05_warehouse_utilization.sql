-- ============================================================
-- Business Question: Which warehouses are over- or under-utilized,
-- and how much storage capacity do we have sitting idle vs.
-- overloaded by region?
--
-- Approach: Aggregate to the Warehouse_ID grain, classify each
-- warehouse with a CASE-based utilization band, then roll that
-- classification up by region.
-- ============================================================

USE supply_chain_db;

-- Per-warehouse utilization classification
WITH warehouse_agg AS (
    SELECT
        Warehouse_ID,
        Warehouse_Location,
        COUNT(*) AS products_stored,
        ROUND(AVG(Utilization_Rate), 2) AS avg_utilization_rate,
        ROUND(AVG(Storage_Capacity), 0) AS avg_storage_capacity
    FROM supply_chain
    GROUP BY Warehouse_ID, Warehouse_Location
)
SELECT
    *,
    CASE
        WHEN avg_utilization_rate >= 80 THEN 'Overutilized'
        WHEN avg_utilization_rate <= 30 THEN 'Underutilized'
        ELSE 'Optimal'
    END AS utilization_band
FROM warehouse_agg
ORDER BY avg_utilization_rate DESC
LIMIT 15;

-- Insight: every warehouse lands in the high-50s% average and none crosses
-- the 80%/30% bands (confirmed below — all 499 come back "Optimal"). This
-- is consistent with the Phase 4 finding that Utilization_Rate is assigned
-- independently per row rather than being a stable warehouse property:
-- averaging ~400 random rows per warehouse converges everyone toward the
-- dataset mean. A real over/underutilization signal would need utilization
-- to be tracked at the warehouse level, not the product-row level.

-- Regional roll-up: how many warehouses in each region fall into each band
WITH warehouse_agg AS (
    SELECT
        Warehouse_ID,
        Warehouse_Location,
        ROUND(AVG(Utilization_Rate), 2) AS avg_utilization_rate
    FROM supply_chain
    GROUP BY Warehouse_ID, Warehouse_Location
),
banded AS (
    SELECT
        Warehouse_Location,
        CASE
            WHEN avg_utilization_rate >= 80 THEN 'Overutilized'
            WHEN avg_utilization_rate <= 30 THEN 'Underutilized'
            ELSE 'Optimal'
        END AS utilization_band
    FROM warehouse_agg
)
SELECT Warehouse_Location, utilization_band, COUNT(*) AS warehouse_count
FROM banded
GROUP BY Warehouse_Location, utilization_band
ORDER BY Warehouse_Location, utilization_band;

-- Insight: all 499 warehouses (across all 4 regions) fall into "Optimal" —
-- confirms the averaging effect above. Worth flagging in docs/AI-assistant
-- answers as a data limitation rather than reporting a false "no problem
-- warehouses" conclusion.
