from typing import List
from daipecore.lineage.DecoratorParserInterface import DecoratorParserInterface


class DecoratorParserResolver:
    def __init__(self, decorator_parsers: List[DecoratorParserInterface]):
        self.__decorator_parsers = {decorator_parser.get_name(): decorator_parser for decorator_parser in decorator_parsers}

    def resolve(self, decorator_name: str) -> DecoratorParserInterface:
        if decorator_name not in self.__decorator_parsers:
            raise Exception(f"Unexpected decorator name: {decorator_name}")

        return self.__decorator_parsers[decorator_name]

    def get_allowed_decorator_names(self):
        return self.__decorator_parsers.keys()
