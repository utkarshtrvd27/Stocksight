# Stock Market Analytics ETL Pipeline

This folder contains the initial ELT implementation for the Stock Market Analytics project.
The pipeline uses a Bronze/Silver/Gold pattern:

- `Bronze` stores raw NSE API output
- `Silver` stores cleaned and transformed data in Delta format
- `Gold` provides analytical views and business-ready aggregations
