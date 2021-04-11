import pyspark.sql.functions as f
from pyspark.sql import DataFrame
from datalakebundle.notebook.decorators import transformation, read_table, table_overwrite


@transformation(read_table("sample_db.sample_table"))
@table_overwrite("sample_db.sample_output_table2")
def load_and_write(df: DataFrame):
    return df.withColumn("INSERT_TS", f.current_timestamp())
