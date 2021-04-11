import ast
from lineagebundle.notebook.decorator.DecoratorParserResolver import DecoratorParserResolver
from lineagebundle.notebook.decorator.Function import Function


class FunctionCollector(ast.NodeVisitor):
    def __init__(self, decorator_parser_resolver: DecoratorParserResolver):
        self.__decorator_parser_resolver = decorator_parser_resolver
        self.__results = []

    @property
    def results(self):
        return self.__results

    def visit_FunctionDef(self, node: ast.FunctionDef):  # noqa: N802
        if (
            not hasattr(node, "decorator_list")
            or not node.decorator_list
            or not [decorator for decorator in node.decorator_list if hasattr(decorator.func, "id")]
        ):
            return

        function_name = node.name
        decorators = [
            decorator
            for decorator in node.decorator_list
            if decorator.func.id in self.__decorator_parser_resolver.get_allowed_decorator_names()
        ]

        self.__results.append(self.__create_func(function_name, decorators))

    def __create_func(self, function_name: str, decorators: list):
        def parse(decorator):
            decorator_parser = self.__decorator_parser_resolver.resolve(decorator.func.id)
            return decorator_parser.parse(decorator)

        return Function(function_name, [parse(decorator) for decorator in decorators])
