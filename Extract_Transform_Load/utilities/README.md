# Utilities

This folder contains shared utility functions and configurations used across all layers.

## Contents

- **validators.py**: Data quality validation functions
- **transformers.py**: Data transformation and feature engineering utilities
- **configs.py**: Configuration loading utilities
- **logging_config.py**: Structured logging setup for Databricks

## Usage

Import these modules in your notebooks:

```python
from utilities.validators import validate_ohlc
from utilities.transformers import add_governance_columns
from utilities.configs import load_config
from utilities.logging_config import logger
```