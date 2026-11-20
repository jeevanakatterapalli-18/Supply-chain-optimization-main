-- Phase 4: SQL Database Creation
--
-- Schema design note:
-- During Phase 3 profiling we verified that Supplier_ID and Warehouse_ID do
-- NOT have stable 1:1 attribute relationships in this dataset (e.g. a single
-- Warehouse_ID appears across all 4 Warehouse_Location values, and
-- Supplier_Rating varies row-to-row for the same Supplier_ID). Building
-- separate dim_supplier / dim_warehouse tables would fabricate a
-- relationship the data doesn't actually have. Instead we use a single,
-- well-typed fact table at the natural grain of the source data (one row
-- per Product_ID snapshot). Phase 5 will demonstrate JOINs, CTEs, and window
-- functions through query logic rather than forced normalization.

CREATE DATABASE IF NOT EXISTS supply_chain_db;
USE supply_chain_db;

DROP TABLE IF EXISTS supply_chain;

CREATE TABLE supply_chain (
    Product_ID                      VARCHAR(20)     NOT NULL,
    Product_Category                VARCHAR(20)     NOT NULL,
    Brand                           VARCHAR(50)     NOT NULL,
    SKU                              VARCHAR(20)     NOT NULL,

    Current_Stock                   INT             NOT NULL,
    Reorder_Level                   INT             NOT NULL,
    Safety_Stock                    INT             NOT NULL,
    Inventory_Turnover              DECIMAL(6,2)    NOT NULL,

    Supplier_ID                     VARCHAR(20)     NOT NULL,
    Supplier_Rating                 DECIMAL(4,2)    NOT NULL,
    Supplier_Performance_Score      DECIMAL(6,2)    NOT NULL,

    Lead_Time_Days                  INT             NOT NULL,

    Warehouse_ID                    VARCHAR(20)     NOT NULL,
    Warehouse_Location              VARCHAR(20)     NOT NULL,
    Storage_Capacity                INT             NOT NULL,
    Utilization_Rate                DECIMAL(6,2)    NOT NULL,

    Units_Sold                      INT             NOT NULL,
    Daily_Demand                    INT             NOT NULL,
    Monthly_Demand                  INT             NOT NULL,
    Seasonal_Demand_Index           DECIMAL(6,2)    NOT NULL,

    Shipping_Cost_USD               DECIMAL(10,2)   NOT NULL,
    Transportation_Mode              VARCHAR(10)     NOT NULL,
    Delivery_Time_Days              INT             NOT NULL,
    On_Time_Delivery_Rate           DECIMAL(6,2)    NOT NULL,

    Product_Cost_USD                DECIMAL(10,2)   NOT NULL,
    Selling_Price_USD               DECIMAL(10,2)   NOT NULL,
    Revenue_USD                     DECIMAL(14,2)   NOT NULL,
    Profit_USD                      DECIMAL(14,2)   NOT NULL,

    Stockout_Risk                   DECIMAL(6,2)    NOT NULL,
    Overstock_Risk                  DECIMAL(6,2)    NOT NULL,
    Supply_Disruption_Risk          DECIMAL(6,2)    NOT NULL,

    Order_Date                      DATE            NOT NULL,
    Month                           TINYINT         NOT NULL,
    Quarter                         TINYINT         NOT NULL,
    Year                            SMALLINT        NOT NULL,

    Demand_Forecast                 INT             NOT NULL,
    Inventory_Optimization_Score    DECIMAL(6,2)    NOT NULL,
    Supply_Chain_Efficiency         DECIMAL(6,2)    NOT NULL,
    Sustainability_Score            DECIMAL(6,2)    NOT NULL,
    Predicted_Reorder_Quantity      INT             NOT NULL,
    Operational_Risk_Score          DECIMAL(6,2)    NOT NULL,

    -- Derived in Phase 3 (python/02_data_cleaning.py)
    Delivery_Date                   DATE            NOT NULL,
    Shipment_Status                 VARCHAR(10)     NOT NULL,
    Customer_Region                 VARCHAR(20)     NOT NULL,
    Is_Loss_Making                  BOOLEAN         NOT NULL,

    PRIMARY KEY (Product_ID),
    INDEX idx_supplier (Supplier_ID),
    INDEX idx_warehouse (Warehouse_ID),
    INDEX idx_category (Product_Category),
    INDEX idx_order_date (Order_Date),
    INDEX idx_shipment_status (Shipment_Status)
);
