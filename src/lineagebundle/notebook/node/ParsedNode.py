class ParsedNode:
    def __init__(self, name: str, input_table: str = None, output_table: str = None):
        self._name = name
        self._input_table = input_table
        self._output_table = output_table

    @property
    def name(self):
        return self._name

    @property
    def input_table(self):
        return self._input_table

    @property
    def output_table(self):
        return self._output_table
