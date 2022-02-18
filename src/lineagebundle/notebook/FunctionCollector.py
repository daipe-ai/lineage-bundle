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

    def visit_FunctionDef(self, node: ast.FunctionDef):  # pylint: disable = invalid-name
        def has_daipe_decorator(decorator):
            return hasattr(decorator.func, "id") or hasattr(decorator.func, "attr")

        if (
            not hasattr(node, "decorator_list")
            or not node.decorator_list
            or not [decorator for decorator in node.decorator_list if has_daipe_decorator(decorator)]
        ):
            return

        allowed_decorator_names = self.__decorator_parser_resolver.get_allowed_decorator_names()

        function_name = node.name

        def is_allowed_decorator(decorator):
            return (hasattr(decorator.func, "id") and decorator.func.id in allowed_decorator_names) or (
                hasattr(decorator.func, "attr") and decorator.func.attr in allowed_decorator_names
            )

        decorators = [decorator for decorator in node.decorator_list if is_allowed_decorator(decorator)]

        self.__results.append(self.__create_func(function_name, decorators))

    def __create_func(self, function_name: str, decorators: list):
        def parse(decorator):
            decorator_name = decorator.func.attr if hasattr(decorator.func, "attr") else decorator.func.id

            decorator_parser = self.__decorator_parser_resolver.resolve(decorator_name)
            return decorator_parser.parse(decorator)

        return Function(function_name, [parse(decorator) for decorator in decorators])
