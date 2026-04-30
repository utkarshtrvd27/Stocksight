# Bronze Layer

This layer stores raw NSE API data in Delta format as the Bronze dataset.

## Contents

- **notebooks/**: Databricks notebooks for data extraction
- **configs/**: Configuration files for API endpoints and storage
- **README.md**: This documentation

## Process

1. Extract raw data from NSE API using `extract_api_daily_nse_data.ipynb`
2. Normalize the nested JSON response using pandas
3. Add governance metadata (`ingestion_timestamp`, `ingestion_date`, `pipeline_run_id`, `source_system`, `file_name`)
4. Write the dataset to a Bronze Delta table in Azure Databricks

## Data Format

Raw NSE API response is flattened into a tabular schema and written as Delta to support Bronze layer querying, lineage, and auditability.

## Notes

- The notebook loads configuration from `configs/bronze_config.yaml`
- The Bronze table is registered as `stock_market.bronze_nse_stock_raw`
- Partitioning is applied by `ingestion_date` for query performance
