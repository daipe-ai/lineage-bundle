from typing import List
from daipecore.lineage.argument.ArgumentMappingInterface import ArgumentMappingInterface


class ArgumentClassResolver:
    def __init__(self, argument_mappings: List[ArgumentMappingInterface]):
        all_mapping = dict()

        for argument_mapping in argument_mappings:
            all_mapping = {**all_mapping, **argument_mapping.get_mapping()}

        self.__argument_mappings = all_mapping

    def resolve(self, function_name: str):
        if function_name not in self.__argument_mappings:
            raise Exception(f"Unexpected function argument name: {function_name}")

        return self.__argument_mappings[function_name]
