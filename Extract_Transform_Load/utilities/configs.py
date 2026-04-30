import yaml
import logging
from pathlib import Path

def load_config(config_path: str) -> dict:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to YAML config file
    
    Returns:
        Configuration dictionary
    """
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def setup_logging(level: str = "INFO", format_str: str = "%(asctime)s - %(levelname)s - %(message)s"):
    """
    Setup logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        format_str: Log format string
    """
    logging.basicConfig(level=getattr(logging, level.upper()), format=format_str)