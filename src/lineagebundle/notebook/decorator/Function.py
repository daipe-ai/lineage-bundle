from typing import Optional
from daipecore.lineage.InputDecoratorInterface import InputDecoratorInterface
from daipecore.lineage.OutputDecoratorInterface import OutputDecoratorInterface
from daipecore.lineage.argument.DecoratorInputFunctionInterface import DecoratorInputFunctionInterface
from daipecore.lineage.argument.FunctionLink import FunctionLink
from lineagebundle.notebook.function.ParsedNotebookFunctionsRelation import ParsedNotebookFunctionsRelation
from lineagebundle.notebook.function.ParsedNotebookFunction import ParsedNotebookFunction


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

        return [
            ParsedNotebookFunctionsRelation(arg.linked_function, self.__name)
            for arg in self.__input_decorator.args
            if isinstance(arg, FunctionLink)
        ]

    def get_nodes(self):
        return [ParsedNotebookFunction(self.__name, self.__get_input_tables(), self.__get_output_table())]

    def __get_input_tables(self):
        if not self.__input_decorator:
            return None

        read_table_args = [arg for arg in self.__input_decorator.args if isinstance(arg, DecoratorInputFunctionInterface)]

        if not read_table_args:
            return None

        return [read_table_arg.identifier for read_table_arg in read_table_args]

    def __get_output_table(self):
        if not self.__output_decorator:
            return None

        return self.__output_decorator.identifier
