import ast
from pathlib import Path
from lineagebundle.notebook.FunctionCollector import FunctionCollector
from lineagebundle.notebook.decorator.DecoratorParserResolver import DecoratorParserResolver


class NotebookParser:
    def __init__(self, decorator_parser_resolver: DecoratorParserResolver):
        self.__decorator_parser_resolver = decorator_parser_resolver

    def parse(self, notebook_path: Path):
        with notebook_path.open("r", encoding="utf-8") as f:
            module = f.read()
        tree = ast.parse(module)
        collector = FunctionCollector(self.__decorator_parser_resolver)
        collector.visit(tree)

        return collector.results
