from daipecore.decorator.notebook_function import notebook_function
from datalakebundle.table.parameters.table_params import table_params


@notebook_function(
    table_params("bronze_covid.tbl_template_2_confirmed_cases").base_date,
)
def load_sample_table(base_date: str):
    print(base_date)
