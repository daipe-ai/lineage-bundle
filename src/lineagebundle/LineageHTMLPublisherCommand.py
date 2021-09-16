from argparse import Namespace
from consolebundle.ConsoleCommand import ConsoleCommand
from lineagebundle.LineageGenerator import LineageGenerator
from lineagebundle.notebook.Notebook import Notebook
from lineagebundle.notebook.function.NotebookFunction import NotebookFunction
from lineagebundle.notebook.function.NotebookFunctionsRelation import NotebookFunctionsRelation
from lineagebundle.pipeline.NotebooksRelation import NotebooksRelation
from lineagebundle.publish.NotebookDetailHTMLParser import NotebookDetailHTMLParser
from lineagebundle.publish.PipelinesHTMLParser import PipelinesHTMLParser
from logging import Logger
from pathlib import Path
from sqlalchemybundle.entity.Base import Base
from typing import List


class LineageHTMLPublisherCommand(ConsoleCommand):
    def __init__(
        self,
        logger: Logger,
        lineage_generator: LineageGenerator,
        pipelines_html_parser: PipelinesHTMLParser,
        notebook_detail_html_parser: NotebookDetailHTMLParser,
    ):
        self.__logger = logger
        self.__lineage_generator = lineage_generator
        self.__pipelines_html_parser = pipelines_html_parser
        self.__notebook_detail_html_parser = notebook_detail_html_parser

    def get_command(self) -> str:
        return "lineage:publish:html"

    def get_description(self):
        return "Creates lineage as a HTML page"

    def run(self, input_args: Namespace):
        entities = self.__lineage_generator.generate_entities()

        notebooks = list(filter(lambda x: isinstance(x, Notebook), entities))
        edges = list(filter(lambda x: isinstance(x, NotebooksRelation), entities))

        layers = list(set(node.layer for node in notebooks))

        html = self.__pipelines_html_parser.parse(layers, notebooks, edges)

        Path("lineage/notebooks").mkdir(parents=True, exist_ok=True)

        with open("lineage/index.html", "w") as file:
            self.__logger.info(f"Writing {file.name}")
            file.write(html)

        for notebook in notebooks:
            self.__create_notebook_detail(notebook, entities)

    def __create_notebook_detail(self, notebook: Notebook, entities: List[Base]):
        notebook_functions = list(filter(lambda x: isinstance(x, NotebookFunction) and x.notebook == notebook, entities))
        notebook_functions_relations = list(filter(lambda x: isinstance(x, NotebookFunctionsRelation) and x.notebook == notebook, entities))

        with open(f"lineage/notebooks/{notebook.label.replace('/', '_')}.html", "w") as file:
            html = self.__notebook_detail_html_parser.parse(notebook_functions, notebook_functions_relations)
            self.__logger.info(f"Writing {file.name}")
            file.write(html)
