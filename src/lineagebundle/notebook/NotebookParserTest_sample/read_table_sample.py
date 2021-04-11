from pyspark.sql import DataFrame
from datalakebundle.notebook.decorators import transformation, read_table


@transformation(read_table("sample_db.sample_table"))
def table_loader(df: DataFrame):
    return df.dropDuplicates()
