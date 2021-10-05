from argparse import Namespace
from consolebundle.ConsoleCommand import ConsoleCommand
from lineagebundle.lineage.LineageGenerator import LineageGenerator
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
        html_path: str,
        notebooks_subpath: str,
        lineage_generator: LineageGenerator,
        pipelines_html_parser: PipelinesHTMLParser,
        notebook_detail_html_parser: NotebookDetailHTMLParser,
    ):
        self.__logger = logger
        self.__html_path = Path(html_path)
        self.__notebooks_subpath = Path(notebooks_subpath)
        self.__lineage_generator = lineage_generator
        self.__pipelines_html_parser = pipelines_html_parser
        self.__notebook_detail_html_parser = notebook_detail_html_parser
        self.__notebooks_path = self.__html_path.joinpath(self.__notebooks_subpath)

    def get_command(self) -> str:
        return "lineage:publish:html"

    def get_description(self):
        return "Creates lineage as a HTML page"

    def run(self, input_args: Namespace):
        entities = self.__lineage_generator.generate_entities()

        notebooks = list(filter(lambda x: isinstance(x, Notebook), entities))
        edges = list(filter(lambda x: isinstance(x, NotebooksRelation), entities))

        layers = list(set(node.layer for node in notebooks))

        html = self.__pipelines_html_parser.parse(layers, notebooks, edges, on_tap_enabled=True)

        self.__notebooks_path.mkdir(parents=True, exist_ok=True)

        index_path = self.__html_path.joinpath(Path("index.html"))
        with index_path.open("w") as file:
            self.__logger.info(f"Writing {file.name}")
            file.write(html)

        for notebook in notebooks:
            self.__create_notebook_detail(notebook, entities)

    def __create_notebook_detail(self, notebook: Notebook, entities: List[Base]):
        notebook_functions = list(filter(lambda x: isinstance(x, NotebookFunction) and x.notebook == notebook, entities))
        notebook_functions_relations = list(filter(lambda x: isinstance(x, NotebookFunctionsRelation) and x.notebook == notebook, entities))

        with self.__notebooks_path.joinpath(Path(f"{notebook.label.replace('/', '_')}.html")).open("w") as file:
            html = self.__notebook_detail_html_parser.parse(notebook_functions, notebook_functions_relations)
            self.__logger.info(f"Writing {file.name}")
            file.write(html)
