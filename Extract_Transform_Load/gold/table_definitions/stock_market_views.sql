-- Transformation views for Stock Market Analytics
-- Use these view definitions in Databricks or Spark SQL to create reusable analytical datasets.

CREATE OR REPLACE VIEW stock_market.vw_nse_stock_daily_summary AS
SELECT
  symbol,
  CAST(tradingDate AS DATE) AS trade_date,
  FIRST(open) AS open_price,
  MAX(high) AS high_price,
  MIN(low) AS low_price,
  LAST(close) AS close_price,
  SUM(tradedQuantity) AS total_quantity,
  SUM(tradedValue) AS total_value,
  AVG(perChange) AS avg_percent_change,
  MAX(weekHigh) AS week_high,
  MIN(weekLow) AS week_low,
  source_system,
  ingestion_timestamp,
  pipeline_run_id
FROM stock_market.silver_nse_stock_processed
GROUP BY symbol, CAST(tradingDate AS DATE), source_system, ingestion_timestamp, pipeline_run_id;

CREATE OR REPLACE VIEW stock_market.vw_nse_stock_technical_indicators AS
SELECT
  symbol,
  trade_date,
  close,
  AVG(close) OVER (PARTITION BY symbol ORDER BY trade_date ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) AS sma_5,
  AVG(close) OVER (PARTITION BY symbol ORDER BY trade_date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) AS sma_20,
  STDDEV(close) OVER (PARTITION BY symbol ORDER BY trade_date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) AS volatility_20,
  RANK() OVER (PARTITION BY symbol ORDER BY trade_date DESC) AS row_rank
FROM stock_market.vw_nse_stock_daily_summary;
