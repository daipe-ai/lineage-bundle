import json
from argparse import Namespace
from consolebundle.ConsoleCommand import ConsoleCommand
from lineagebundle.lineage.LineageGenerator import LineageGenerator
from logging import Logger
from pathlib import Path


class LineageJSONPublisherCommand(ConsoleCommand):
    def __init__(
        self,
        logger: Logger,
        lineage_generator: LineageGenerator,
    ):
        self.__logger = logger
        self.__lineage_generator = lineage_generator

    def get_command(self) -> str:
        return "lineage:publish:json"

    def get_description(self):
        return "Creates lineage as a JSON"

    def run(self, input_args: Namespace):
        notebooks = self.__lineage_generator.get_notebooks()
        notebook_relations, notebook_functions, notebook_function_relations = self.__lineage_generator.get_notebook_relations(notebooks)

        dictionary = {
            "notebooks": [{"label": notebook.label, "path": notebook.path, "layer": notebook.layer} for notebook in notebooks],
            "notebook_relations": [
                {"source": notebook_relation.source.label, "target": notebook_relation.target.label}
                for notebook_relation in notebook_relations
            ],
            "notebook_functions": [
                {"name": notebook_function.name, "notebook": notebook_function.notebook.label} for notebook_function in notebook_functions
            ],
            "notebook_function_relations": [
                {
                    "source": notebook_functions_relation.source,
                    "target": notebook_functions_relation.target,
                    "notebook": notebook_functions_relation.notebook.label,
                }
                for notebook_functions_relation in notebook_function_relations
            ],
        }

        json_path = Path("lineage")
        json_path.mkdir(parents=True, exist_ok=True)

        with json_path.joinpath(Path("lineage.json")).open("w") as json_file:
            self.__logger.info(f"Writing {json_file.name}")
            json.dump(dictionary, json_file)
