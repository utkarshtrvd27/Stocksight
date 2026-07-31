import os
import sys
from datetime import date, datetime
from pathlib import Path
import psycopg2
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, col, coalesce, concat_ws, lit, sha2, max

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ETL_Pipeline.bronze.landing2bronze import load_env_file, get_last_ingest_partition, write_to_elt_config

# --- CONFIGURATION SECTION ---
ENV_PATH = PROJECT_ROOT / ".env"
load_env_file(ENV_PATH)

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DB_URL = f"jdbc:postgresql://{DB_HOST}:{DB_PORT}/{DB_NAME}"
DB_PROPERTIES = {
    "user": DB_USER,
    "password": DB_PASSWORD,
    "driver": "org.postgresql.Driver"
}
# Path to your downloaded PostgreSQL JDBC Driver Jar
JDBC_JAR_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../drivers/postgresql-42.7.13.jar")

def ensure_silver_schema_exists() -> None:
    """Create the silver schema in PostgreSQL if it does not already exist."""
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            cur.execute("CREATE SCHEMA IF NOT EXISTS silver")
    finally:
        conn.close()
        
def get_data_from_bronze(spark: SparkSession, table_name: str, latest_ingest_partition: date):
    if latest_ingest_partition is not None:
        if not isinstance(latest_ingest_partition, date):
            latest_ingest_partition = datetime.strptime(str(latest_ingest_partition), "%Y-%m-%d").date()

        partition_value = latest_ingest_partition.strftime("%Y-%m-%d")
        query = f"""
            SELECT *
            FROM bronze.{table_name}
            WHERE "BizDt" > '{partition_value}'
        """
    else:
        query = f"SELECT * FROM bronze.{table_name}"

    return spark.read \
        .format("jdbc") \
        .option("url", DB_URL) \
        .option("dbtable", f"({query}) AS bronze_data") \
        .option("user", DB_USER) \
        .option("password", DB_PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .load()
        
def main():
    log_file_path = os.path.abspath("ETL_Pipeline/bronze/conf/log4j2.properties")
    # print("Correct log_path:", log_file_path)
    
    if os.name == 'nt':
        log_file_path = log_file_path.replace("\\", "/")

    os.environ["SPARK_SUBMIT_OPTS"] = f"-Dlog4j2.configurationFile=file:///{log_file_path}"
    
    spark = SparkSession.builder \
        .appName("Bronze to Silver ETL") \
        .config("spark.jars", JDBC_JAR_PATH) \
        .getOrCreate()
    
    print("PySpark Session started successfully.\n")
    
    ensure_silver_schema_exists()
    print("Silver schema exists.\n")
    
    # Connect to the bronze layer and read data
    print("Reading data from bronze.indianstocks table...")
    
    # Incremental data loading from bronze table
    last_ingest_record = get_last_ingest_partition("silver", "indianstocks", "daily")
    last_ingest_partition = last_ingest_record["ingest_partition"] if last_ingest_record else None

    silver_df = get_data_from_bronze(spark, "indianstocks", last_ingest_partition)
    print("Data read from bronze.indianstocks table was successful.")
    print(f"Total new records to write: {silver_df.count()}\n")
    
    # Dropping unnecessary columns
    silver_df = silver_df.drop('Sgmt', 'FinInstrmTp', 'FinInstrmId', 'FininstrmActlXpryDt', 'StrkPric', 'OptnTp',
        'UndrlygPric', 'SttlmPric', 'OpnIntrst', 'ChngInOpnIntrst', 'NewBrdLotQty', 'Rmks', 'Rsvd1', 'Rsvd2',
        'Rsvd3', 'Rsvd4', 'SsnId', '_source_file')
    
    # Transforming Column names
    silver_df = silver_df.withColumnRenamed("TradDt", "trading_date") \
        .withColumnRenamed("BizDt", "business_date") \
        .withColumnRenamed("Src", "data_source_code") \
        .withColumnRenamed("TckrSymb", "ticker_symbol") \
        .withColumnRenamed("SctySrs", "security_series") \
        .withColumnRenamed("XpryDt", "expiry_date") \
        .withColumnRenamed("FinInstrmNm", "financial_instrument_name") \
        .withColumnRenamed("OpnPric", "open_price") \
        .withColumnRenamed("HghPric", "high_price") \
        .withColumnRenamed("LwPric", "low_price") \
        .withColumnRenamed("ClsPric", "closing_price") \
        .withColumnRenamed("LastPric", "last_price") \
        .withColumnRenamed("PrvsClsgPric", "previous_closing_price") \
        .withColumnRenamed("TtlTradgVol", "total_trading_volume") \
        .withColumnRenamed("TtlTrfVal", "total_turnover_value") \
        .withColumnRenamed("TtlNbOfTxsExctd", "total_number_of_transactions_executed") \
        .withColumnRenamed("_ingested_at", "ingestion_date_time")
    
    # Adding New Columns
    hash_columns = ["data_source_code", "ISIN", "ticker_symbol", "business_date"]

    hash_input = concat_ws(
        "|",
        *[coalesce(col(c).cast("string"), lit("")) for c in hash_columns]
    )

    silver_df = silver_df.withColumn("silver_load_date_time", current_timestamp()) \
        .withColumn("hash_key", sha2(hash_input, 256))
        
    # Filtering out records with Security Series as 'EQ' and 'SM' only
    silver_df = silver_df.filter(col("security_series").isin("EQ", "SM"))
    
    # Dropping duplicate records based on the hash_key
    silver_df = silver_df.dropDuplicates(["hash_key"])

    silver_df.write \
            .mode("append") \
            .jdbc(url=DB_URL, table="silver.indianstocks", properties=DB_PROPERTIES)

    # Updating the ELT configuration with the latest partition
    latest_partition_row = silver_df.agg(max("business_date").alias("max_business_date")).collect()[0]
    latest_partition_date = latest_partition_row["max_business_date"]
    
    if latest_partition_date is not None:
        if not isinstance(latest_partition_date, date):
            latest_partition_date = datetime.strptime(str(latest_partition_date), "%Y-%m-%d").date()
        write_to_elt_config("silver", "indianstocks", "daily", latest_partition_date)
    
        print("ELT config table has been updated with the latest partition.")
    else:
        print("No new records were found to update the ELT config table.")

if __name__ == "__main__":
    main()