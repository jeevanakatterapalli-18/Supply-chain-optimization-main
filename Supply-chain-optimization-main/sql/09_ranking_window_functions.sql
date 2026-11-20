-- ============================================================
-- Business Question: Within each product category, which are
-- the top revenue-generating products, and how does a product's
-- rank compare across different metrics (revenue vs. profit)?
--
-- Approach: A focused demonstration of ranking window functions
-- (ROW_NUMBER, RANK, DENSE_RANK, PERCENT_RANK) side by side on
-- the same partition so the difference between them is visible
-- directly in the output.
-- ============================================================

USE supply_chain_db;

-- Top 3 products by revenue within each category (ROW_NUMBER + PARTITION BY)
WITH product_rank AS (
    SELECT
        Product_Category,
        Product_ID,
        Revenue_USD,
        ROW_NUMBER() OVER (PARTITION BY Product_Category ORDER BY Revenue_USD DESC) AS rn
    FROM supply_chain
)
SELECT Product_Category, Product_ID, Revenue_USD, rn AS rank_in_category
FROM product_rank
WHERE rn <= 3
ORDER BY Product_Category, rn;

-- Insight: every category's #1 product tops out right at the ~$499,990-
-- $500,000 ceiling (Revenue_USD's max observed in profiling is $499,996.33)
-- — the "best" product per category is really "whichever product happened
-- to land near the generated maximum," not a standout performer relative
-- to its category peers, given revenue is close to uniformly distributed.

-- RANK vs DENSE_RANK vs PERCENT_RANK side by side, ranking suppliers by
-- total revenue — illustrates how each handles ties/scale differently
WITH supplier_revenue AS (
    SELECT Supplier_ID, SUM(Revenue_USD) AS total_revenue
    FROM supply_chain
    GROUP BY Supplier_ID
)
SELECT
    Supplier_ID,
    total_revenue,
    RANK()       OVER (ORDER BY total_revenue DESC) AS rank_with_gaps,
    DENSE_RANK() OVER (ORDER BY total_revenue DESC) AS dense_rank_no_gaps,
    ROUND(PERCENT_RANK() OVER (ORDER BY total_revenue DESC) * 100, 2) AS percentile_from_top
FROM supplier_revenue
ORDER BY total_revenue DESC
LIMIT 15;

-- Insight: RANK and DENSE_RANK agree here because there happen to be no
-- exact revenue ties among top suppliers (no gaps to see) — but they would
-- diverge the moment two suppliers tied on total_revenue, which is the
-- actual reason to pick DENSE_RANK for a "top N tiers" report and RANK
-- for a strict leaderboard position.
