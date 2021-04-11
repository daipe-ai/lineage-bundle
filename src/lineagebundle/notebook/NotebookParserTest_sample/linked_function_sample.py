import pyspark.sql.functions as f
from pyspark.sql import DataFrame
from datalakebundle.notebook.decorators import transformation, read_table


@transformation(read_table("sample_db.sample_table"))
def load_sample_table(df: DataFrame):
    return df.withColumn("new_column", "old_column")


@transformation(load_sample_table)
def add_timestamp(df: DataFrame):
    return df.withColumn("INSERT_TS", f.current_timestamp())
