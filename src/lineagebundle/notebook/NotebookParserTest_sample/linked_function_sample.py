import pyspark.sql.functions as f
from datalakebundle.notebook.decorator.transformation import transformation
from datalakebundle.table.read.table_reader import read_table
from pyspark.sql import DataFrame


@transformation(read_table("sample_db.sample_table"))
def load_sample_table(df: DataFrame):
    return df.withColumn("new_column", f.col("old_column"))


@transformation(load_sample_table)
def add_timestamp(df: DataFrame):
    return df.withColumn("INSERT_TS", f.current_timestamp())
