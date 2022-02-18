from lineagebundle.lineage.LineageGenerator import LineageGenerator
from lineagebundle.notebook.Notebook import Notebook
from lineagebundle.html.PipelinesHTMLParser import PipelinesHTMLParser
from typing import List


class HTMLCreator:
    def __init__(
        self,
        lineage_generator: LineageGenerator,
        pipelines_html_parser: PipelinesHTMLParser,
    ):
        self.__lineage_generator = lineage_generator
        self.__pipelines_html_parser = pipelines_html_parser

    def create_pipelines_html_code(self, notebooks: List[Notebook], on_tap_enabled: bool = True):
        edges = list(
            filter(
                lambda relation: relation.target in notebooks and relation.source in notebooks, self.__lineage_generator.notebooks_relations
            )
        )

        layers = list(set(str(n.layer) for n in notebooks))

        return self.__pipelines_html_parser.parse(layers, notebooks, edges, on_tap_enabled)
