# Silver Layer

This layer stores cleaned, validated, and governed data.

## Contents

- **notebooks/**: Databricks notebooks for validation and cleaning
- **libraries/**: Validation and cleaning functions
- **table_definitions/**: Delta table DDL statements
- **README.md**: This documentation

## Process

1. Read raw data from Bronze layer
2. Apply data quality validations (OHLC logic, null checks)
3. Clean data (remove unnecessary columns, filter invalid records)
4. Add governance metadata (pipeline_run_id, source_system, etc.)
5. Write to Delta tables with partitioning

## Data Quality Rules

- OHLC validation: `low ≤ close ≤ high`
- Required columns present
- No nulls in critical fields (symbol, close, high, low)
- Data type consistency
