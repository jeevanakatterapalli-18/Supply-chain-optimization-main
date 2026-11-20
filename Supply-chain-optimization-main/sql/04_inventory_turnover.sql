-- ============================================================
-- Business Question: Which categories/products move inventory
-- efficiently, and which are sitting on slow-moving stock that
-- ties up working capital?
--
-- Approach: Average the given Inventory_Turnover metric by
-- category, then use NTILE() to bucket individual products into
-- quartiles so "slow movers" (bottom quartile) can be pulled as
-- a concrete action list.
-- ============================================================

USE supply_chain_db;

-- Average turnover and stock position by category
SELECT
    Product_Category,
    ROUND(AVG(Inventory_Turnover), 2) AS avg_turnover,
    ROUND(AVG(Current_Stock), 0) AS avg_current_stock,
    ROUND(AVG(Reorder_Level), 0) AS avg_reorder_level,
    SUM(CASE WHEN Current_Stock < Reorder_Level THEN 1 ELSE 0 END) AS products_below_reorder_level
FROM supply_chain
GROUP BY Product_Category
ORDER BY avg_turnover DESC;

-- Insight: turnover averages ~10.0 across all 5 categories (no category
-- stands out) and ~40% of products (roughly 2,000 per category) are
-- currently below their reorder level — a flat, category-agnostic
-- restocking problem, not a category-specific one.

-- Quartile-bucket every product by turnover (NTILE window function), then
-- summarize each bucket — bucket 1 = slowest-moving 25% of inventory
WITH turnover_quartiles AS (
    SELECT
        Product_ID, Product_Category, Inventory_Turnover, Current_Stock, Product_Cost_USD,
        NTILE(4) OVER (ORDER BY Inventory_Turnover ASC) AS turnover_quartile
    FROM supply_chain
)
SELECT
    turnover_quartile,
    COUNT(*) AS product_count,
    ROUND(AVG(Inventory_Turnover), 2) AS avg_turnover,
    ROUND(SUM(Current_Stock * Product_Cost_USD), 2) AS capital_tied_up_usd
FROM turnover_quartiles
GROUP BY turnover_quartile
ORDER BY turnover_quartile;

-- Insight: ~$125B of stock value sits in each quartile almost equally
-- (all four within 1% of each other) — the slowest-moving quarter of
-- inventory ties up just as much capital as the fastest-moving quarter,
-- meaning turnover-based prioritization has real capital efficiency upside.

-- Concrete action list: slow-moving products (bottom turnover quartile)
-- carrying high stock value — the best restocking-pause candidates
WITH turnover_quartiles AS (
    SELECT
        Product_ID, Product_Category, Brand, Inventory_Turnover, Current_Stock,
        Product_Cost_USD, ROUND(Current_Stock * Product_Cost_USD, 2) AS stock_value_usd,
        NTILE(4) OVER (ORDER BY Inventory_Turnover ASC) AS turnover_quartile
    FROM supply_chain
)
SELECT Product_ID, Product_Category, Brand, Inventory_Turnover, Current_Stock, stock_value_usd
FROM turnover_quartiles
WHERE turnover_quartile = 1
ORDER BY stock_value_usd DESC
LIMIT 20;
