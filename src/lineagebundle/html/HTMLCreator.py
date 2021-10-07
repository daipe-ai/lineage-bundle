from lineagebundle.lineage.LineageGenerator import LineageGenerator
from lineagebundle.notebook.Notebook import Notebook
from lineagebundle.html.NotebookDetailHTMLParser import NotebookDetailHTMLParser
from lineagebundle.html.PipelinesHTMLParser import PipelinesHTMLParser
from pathlib import Path
from typing import List


class HTMLCreator:
    def __init__(
        self,
        notebooks_subpath: str,
        lineage_generator: LineageGenerator,
        pipelines_html_parser: PipelinesHTMLParser,
        notebook_detail_html_parser: NotebookDetailHTMLParser,
    ):
        self.__notebooks_subpath = Path(notebooks_subpath)
        self.__lineage_generator = lineage_generator
        self.__pipelines_html_parser = pipelines_html_parser
        self.__notebook_detail_html_parser = notebook_detail_html_parser

    def create_pipelines_html_code(self, notebooks: List[Notebook], on_tap_enabled: bool = True):
        edges = self.__lineage_generator.notebooks_relations

        layers = list(set(n.layer for n in notebooks))

        return self.__pipelines_html_parser.parse(layers, notebooks, edges, on_tap_enabled)