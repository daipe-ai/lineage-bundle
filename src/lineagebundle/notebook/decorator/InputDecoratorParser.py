import _ast
from injecta.module import attribute_loader
from lineagebundle.notebook.decorator.ArgumentParser import ArgumentParser
from databricksbundle.notebook.lineage.DecoratorParserInterface import DecoratorParserInterface


class InputDecoratorParser(DecoratorParserInterface):
    def __init__(self, name: str, class_: str, argument_parser: ArgumentParser):
        self.__name = name
        self.__class = class_
        self.__argument_parser = argument_parser

    def parse(self, decorator: _ast.Call):
        args = [self.__argument_parser.parse(arg) for arg in decorator.args]

        pos = self.__class.rfind(".")

        module_name = self.__class[0:pos]
        class_name = self.__class[pos + 1 :]  # noqa: E203

        class_ = attribute_loader.load(module_name, class_name)

        return class_(decorator.func.id, args)

    def get_name(self) -> str:
        return self.__name
