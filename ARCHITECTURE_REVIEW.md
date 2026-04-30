# Stock Market Analytics - Architecture Review

### Medallion Architecture (Recommended)
```
Extract_Transform_Load/
├── bronze/
│   ├── notebooks/
│   │   └── extract_api_daily_nse_data.ipynb
│   ├── configs/
│   │   └── bronze_config.yaml
│   └── README.md
├── silver/
│   ├── notebooks/
│   │   └── transform_daily_nse_data.ipynb
│   ├── table_definitions/
│   │   └── stock_market_delta_tables.sql
│   └── README.md
├── gold/
│   ├── notebooks/
│   │   ├── nse_aggregations.ipynb
│   │   └── nse_feature_engineering.ipynb
│   ├── table_defintions/
│   │   └── stock_market_views.sql
│   └── README.md
├── orchestration/
│   └── jobs/
│       └── daily_stock_pipeline.yml
├── utilities/
│   ├── validators.py
│   ├── transformers.py
│   ├── configs.py
│   └── logging_config.py
└── README.md
```
