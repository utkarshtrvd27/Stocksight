# Gold Layer

This layer stores business-ready aggregations and ML features.

## Contents

- **notebooks/**: Databricks notebooks for aggregations and feature engineering
- **table_definitions/**: SQL view definitions for analytics
- **README.md**: This documentation

## Process

1. Read cleaned data from Silver layer
2. Create business aggregations (daily summaries, technical indicators)
3. Generate ML features (normalized prices, volatility measures)
4. Store as Delta tables and SQL views

## Outputs

- **Daily Stock Summary**: Aggregated OHLCV data by symbol and date
- **Technical Indicators**: SMA, volatility, price changes
- **ML Features**: Normalized and engineered features for modeling
