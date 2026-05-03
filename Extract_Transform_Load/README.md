# Stock Market Analytics ETL Pipeline

This folder contains the initial ELT implementation for the Stock Market Analytics project.
The pipeline uses a Bronze/Silver/Gold pattern:

- `Bronze` stores raw NSE API output
- `Silver` stores cleaned and transformed data in Delta format
- `Gold` provides analytical views and business-ready aggregations

## Files

- `data_sources/api/src2stg_raw_nse_stocks_data.ipynb`
  - Notebook for extracting NSE API data and writing raw JSON output
- `data_sources/api/stg2stg_processed_nse_stocks_data.ipynb`
  - Notebook for processing raw JSON to Parquet and adding governance fields
- `data_sources/api/stock_market_pipeline.py`
  - Python script that automates extraction and processing
- `pub/table_definitions/stock_market_delta_tables.sql`
  - Delta table DDL templates for Bronze/Silver/Gold
- `trans/table_defintions/stock_market_views.sql`
  - SQL views for analytics and derived metrics

## Usage

Extract raw data and process it in one command:

```powershell
python .\data_sources\api\stock_market_pipeline.py --extract --process --raw-dir .\data_sources\api\raw --silver-dir .\data_sources\api\silver
```

To use Delta format for the Silver layer:

```powershell
python .\data_sources\api\stock_market_pipeline.py --process --use-delta --raw-dir .\data_sources\api\raw --silver-dir .\data_sources\api\silver_delta
```

## Next steps

1. Add a Gold layer for aggregated business metrics
2. Configure Azure Databricks mounts for ADLS Gen2
3. Schedule the pipeline with Databricks Jobs or Azure Data Factory
4. Add data quality checks and incremental load support
