-- ============================================================
-- Business Question: Where are shipment delays concentrated —
-- which carrier, warehouse region, or product category is the
-- biggest driver of late deliveries?
--
-- Approach: Compute the delayed rate (Shipment_Status = 'Delayed')
-- as a percentage, sliced by each dimension in turn, so the worst
-- offenders surface immediately instead of scanning raw counts.
-- ============================================================

USE supply_chain_db;

-- Delay rate by transportation mode (carrier)
SELECT
    Transportation_Mode,
    COUNT(*) AS total_shipments,
    SUM(CASE WHEN Shipment_Status = 'Delayed' THEN 1 ELSE 0 END) AS delayed_shipments,
    ROUND(100.0 * SUM(CASE WHEN Shipment_Status = 'Delayed' THEN 1 ELSE 0 END) / COUNT(*), 2) AS delayed_pct
FROM supply_chain
GROUP BY Transportation_Mode
ORDER BY delayed_pct DESC;

-- Delay rate by warehouse region
SELECT
    Warehouse_Location,
    COUNT(*) AS total_shipments,
    SUM(CASE WHEN Shipment_Status = 'Delayed' THEN 1 ELSE 0 END) AS delayed_shipments,
    ROUND(100.0 * SUM(CASE WHEN Shipment_Status = 'Delayed' THEN 1 ELSE 0 END) / COUNT(*), 2) AS delayed_pct
FROM supply_chain
GROUP BY Warehouse_Location
ORDER BY delayed_pct DESC;

-- Delay rate by product category
SELECT
    Product_Category,
    COUNT(*) AS total_shipments,
    SUM(CASE WHEN Shipment_Status = 'Delayed' THEN 1 ELSE 0 END) AS delayed_shipments,
    ROUND(100.0 * SUM(CASE WHEN Shipment_Status = 'Delayed' THEN 1 ELSE 0 END) / COUNT(*), 2) AS delayed_pct
FROM supply_chain
GROUP BY Product_Category
ORDER BY delayed_pct DESC;

-- The 20 costliest delayed shipments — a concrete, actionable list rather
-- than just an aggregate rate
SELECT
    Product_ID, Supplier_ID, Warehouse_ID, Transportation_Mode,
    Lead_Time_Days, Delivery_Time_Days, Shipping_Cost_USD, Order_Date, Delivery_Date
FROM supply_chain
WHERE Shipment_Status = 'Delayed'
ORDER BY Shipping_Cost_USD DESC
LIMIT 20;

-- Insight: delay rate is flat at ~15.3-16% across every carrier, region,
-- and category (max spread <1pp) — there is no single "problem lane"; delays
-- are a systemic ~1-in-6 baseline rather than concentrated in one segment.
-- This matters for the AI assistant phase: a root-cause question like "why
-- are deliveries delayed?" should surface this flatness rather than invent
-- a scapegoat carrier/warehouse that the data doesn't support.
