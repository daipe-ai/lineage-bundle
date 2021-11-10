from argparse import Namespace
from consolebundle.ConsoleCommand import ConsoleCommand
from lineagebundle.lineage.LineageGenerator import LineageGenerator
from lineagebundle.notebook.Notebook import Notebook
from lineagebundle.html.NotebookDetailHTMLParser import NotebookDetailHTMLParser
from lineagebundle.html.PipelinesHTMLParser import PipelinesHTMLParser
from logging import Logger
from pathlib import Path


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
        notebooks = self.__lineage_generator.notebooks
        edges = self.__lineage_generator.notebooks_relations

        layers = list(set(node.layer for node in notebooks))

        html = self.__pipelines_html_parser.parse(layers, notebooks, edges, on_tap_enabled=True)

        self.__notebooks_path.mkdir(parents=True, exist_ok=True)

        index_path = self.__html_path.joinpath(Path("index.html"))
        with index_path.open("w") as file:
            self.__logger.info(f"Writing {file.name}")
            file.write(html)

        for notebook in notebooks:
            self.__create_notebook_detail(notebook)

    def __create_notebook_detail(self, notebook: Notebook):
        notebook_functions = list(filter(lambda function: function.notebook == notebook, self.__lineage_generator.notebook_functions))
        notebook_functions_relations = list(
            filter(lambda relation: relation.notebook == notebook, self.__lineage_generator.notebook_functions_relations)
        )

        with self.__notebooks_path.joinpath(Path(f"{notebook.label.replace('/', '_')}.html")).open("w") as file:
            html = self.__notebook_detail_html_parser.parse(notebook_functions, notebook_functions_relations)
            self.__logger.info(f"Writing {file.name}")
            file.write(html)
