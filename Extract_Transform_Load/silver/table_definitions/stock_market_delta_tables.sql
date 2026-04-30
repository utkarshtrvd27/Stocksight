-- Delta table definitions for Stock Market Analytics
-- Use these definitions in Azure Databricks or on any Spark environment with Delta Lake enabled.

CREATE DATABASE IF NOT EXISTS stock_market;

CREATE TABLE IF NOT EXISTS stock_market.bronze_nse_stock_raw
USING DELTA
LOCATION '/mnt/stockdata/bronze/nse_stock_raw'
AS SELECT * FROM parquet.`/mnt/stockdata/bronze/nse_stock_raw`;

CREATE TABLE IF NOT EXISTS stock_market.silver_nse_stock_processed
USING DELTA
LOCATION '/mnt/stockdata/silver/nse_stock_processed'
AS SELECT * FROM parquet.`/mnt/stockdata/silver/nse_stock_processed`;

CREATE TABLE IF NOT EXISTS stock_market.gold_stock_daily_summary (
    symbol STRING,
    tradeDate DATE,
    openPrice DOUBLE,
    highPrice DOUBLE,
    lowPrice DOUBLE,
    closePrice DOUBLE,
    tradedQuantity BIGINT,
    tradedValue DOUBLE,
    percentChange DOUBLE,
    source_system STRING,
    ingestion_timestamp TIMESTAMP,
    pipeline_run_id STRING
)
USING DELTA
LOCATION '/mnt/stockdata/gold/stock_daily_summary';

-- Note: Replace /mnt/stockdata with your ADLS Gen2 mount or DBFS path.
-- In Databricks, use CREATE TABLE ... USING DELTA LOCATION 'dbfs:/mnt/...'.
