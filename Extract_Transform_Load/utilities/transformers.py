import pyspark.sql.functions as F
from pyspark.sql.window import Window
import logging

logger = logging.getLogger(__name__)

def add_governance_columns(df, pipeline_run_id: str, source_system: str):
    """
    Add governance metadata columns to DataFrame.
    
    Args:
        df: Spark DataFrame
        pipeline_run_id: Unique pipeline run identifier
        source_system: Source system name
    
    Returns:
        DataFrame with governance columns
    """
    return df \
        .withColumn("ingestion_timestamp", F.current_timestamp()) \
        .withColumn("pipeline_run_id", F.lit(pipeline_run_id)) \
        .withColumn("source_system", F.lit(source_system)) \
        .withColumn("file_name", F.input_file_name())

def calculate_technical_indicators(df):
    """
    Calculate basic technical indicators.
    
    Args:
        df: Spark DataFrame with price data
    
    Returns:
        DataFrame with additional indicator columns
    """
    window_spec = Window.partitionBy("symbol").orderBy("tradingDate")
    
    return df \
        .withColumn("price_change", F.col("close") - F.lag("close").over(window_spec)) \
        .withColumn("price_change_pct", 
                   (F.col("close") - F.lag("close").over(window_spec)) / F.lag("close").over(window_spec) * 100)

def partition_by_date(df, date_col: str = "tradingDate"):
    """
    Add partitioning column based on date.
    
    Args:
        df: Spark DataFrame
        date_col: Date column name
    
    Returns:
        DataFrame with partition column
    """
    return df.withColumn("partition_date", F.to_date(F.col(date_col)))