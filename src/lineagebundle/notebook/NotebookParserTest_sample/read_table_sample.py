from datalakebundle.notebook.decorator.transformation import transformation
from datalakebundle.table.read.table_reader import read_table
from pyspark.sql import DataFrame


@transformation(read_table("sample_db.sample_table"))
def table_loader(df: DataFrame):
    return df.dropDuplicates()
