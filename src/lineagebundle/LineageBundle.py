from box import Box
from injecta.dtype.DType import DType
from injecta.module import attribute_loader
from injecta.service.Service import Service
from injecta.service.ServiceAlias import ServiceAlias
from injecta.service.argument.PrimitiveArgument import PrimitiveArgument
from pyfonybundles.Bundle import Bundle
from typing import List
from pyfonybundles.loader import entry_points_reader
from lineagebundle.notebook.decorator.InputDecoratorParser import InputDecoratorParser


class LineageBundle(Bundle):
    def modify_services(self, services: List[Service], aliases: List[ServiceAlias], parameters: Box):
        all_mapping = self.__get_mapping()
        new_services = self.__prepare_services(all_mapping)

        return services + new_services, aliases

    def __prepare_services(self, all_mapping):
        def extract_class_name(class_):
            return class_.__module__[class_.__module__.rfind(".") + 1 :]  # noqa: E203

        def create_service(decorator_name: str, decorator_class):
            service_name = f"lineagebundle.notebook.decorator.{decorator_name}_parser"
            class_ = DType(InputDecoratorParser.__module__, extract_class_name(InputDecoratorParser))
            decorator_class_name = extract_class_name(decorator_class)

            arguments = [PrimitiveArgument(decorator_name), PrimitiveArgument(decorator_class.__module__ + "." + decorator_class_name)]
            tags = ["lineage.decorator.parser"]

            return Service(service_name, class_, arguments, tags)

        return [create_service(k, v) for k, v in all_mapping.items()]

    def __get_mapping(self):
        decorator_mapping_entry_points = [
            entry_point for entry_point in entry_points_reader.get_by_key("daipe") if entry_point.name == "input_decorators_mapping"
        ]

        all_mapping = dict()

        for decorator_mapping_entry_point in decorator_mapping_entry_points:
            decorator_mapping = attribute_loader.load_from_string(decorator_mapping_entry_point.value)()
            all_mapping = {**all_mapping, **decorator_mapping}

        return all_mapping
