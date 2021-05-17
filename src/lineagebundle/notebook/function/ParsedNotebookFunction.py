from typing import List


class ParsedNotebookFunction:
    def __init__(self, name: str, input_tables: List[str] = None, output_table: str = None):
        self._name = name
        self._input_tables = input_tables or []
        self._output_table = output_table

    @property
    def name(self):
        return self._name

    @property
    def input_tables(self):
        return self._input_tables

    @property
    def output_table(self):
        return self._output_table
