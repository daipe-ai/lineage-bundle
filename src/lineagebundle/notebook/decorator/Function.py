from typing import Optional
from databricksbundle.notebook.lineage.InputDecoratorInterface import InputDecoratorInterface
from databricksbundle.notebook.lineage.OutputDecoratorInterface import OutputDecoratorInterface
from databricksbundle.notebook.lineage.argument.FunctionLink import FunctionLink
from datalakebundle.notebook.lineage.TableWriter import TableWriter
from datalakebundle.notebook.lineage.argument.ReadTable import ReadTable
from lineagebundle.notebook.edge.ParsedEdge import ParsedEdge
from lineagebundle.notebook.node.ParsedNode import ParsedNode


class Function:

    __input_decorator: Optional[InputDecoratorInterface]
    __output_decorator: Optional[OutputDecoratorInterface]

    def __init__(self, name: str, decorators: list):
        self.__name = name
        self.__decorators = decorators

        input_decorators = [decorator for decorator in decorators if isinstance(decorator, InputDecoratorInterface)]
        output_decorators = [decorator for decorator in decorators if isinstance(decorator, OutputDecoratorInterface)]

        self.__input_decorator = input_decorators[0] if input_decorators else None
        self.__output_decorator = output_decorators[0] if output_decorators else None

    @property
    def name(self):
        return self.__name

    @property
    def decorators(self):
        return self.__decorators

    def get_edges(self):
        if not self.__input_decorator:
            return []

        return [ParsedEdge(arg.linked_function, self.__name) for arg in self.__input_decorator.args if isinstance(arg, FunctionLink)]

    def get_nodes(self):
        return [ParsedNode(self.__name, self.__get_input_table(), self.__get_output_table())]

    def __get_input_table(self):
        if not self.__input_decorator:
            return None

        read_table_args = [arg for arg in self.__input_decorator.args if isinstance(arg, ReadTable)]

        if not read_table_args:
            return None

        return read_table_args[0].table_name

    def __get_output_table(self):
        if isinstance(self.__output_decorator, TableWriter):
            return self.__output_decorator.table_name

        return None
