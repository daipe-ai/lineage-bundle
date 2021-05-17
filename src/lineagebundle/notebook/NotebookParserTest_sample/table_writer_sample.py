import pyspark.sql.functions as f
from datalakebundle.notebook.decorator.transformation import transformation
from datalakebundle.table.read.table_reader import read_table
from datalakebundle.table.write.table_overwrite import table_overwrite
from pyspark.sql import DataFrame


@transformation(read_table("sample_db.sample_table"))
@table_overwrite("sample_db.sample_output_table2")
def load_and_write(df: DataFrame):
    return df.withColumn("INSERT_TS", f.current_timestamp())
