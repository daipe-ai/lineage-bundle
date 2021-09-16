import os
from lineagebundle.notebook.Notebook import Notebook
from lineagebundle.notebook.function.NotebookFunctionsRelation import NotebookFunctionsRelation
from lineagebundle.pipeline.NotebooksRelation import NotebooksRelation
from typing import List, Union


class PipelinesHTMLParser:
    def parse(self, layers: List[str], notebooks: List[Notebook], edges: List[NotebooksRelation]) -> str:
        template_path = os.path.join(os.path.dirname(__file__), "templates/template.html")
        with open(template_path) as html_file:
            html = html_file.read()

        return (
            html.replace("NODES_PLACEHOLDER", self.__parse_nodes(notebooks) + "," + self.__parse_layers(layers))
            .replace("EDGES_PLACEHOLDER", self.__parse_edges(edges))
            .replace("HREF_PLACEHOLDER", "'notebooks/' + e.target.data('name') + '.html'")
        )

    def __parse_edges(self, edges: List[Union[NotebooksRelation, NotebookFunctionsRelation]]) -> str:
        def parse(e: Union[NotebooksRelation, NotebookFunctionsRelation]):
            return f"""{{ \
                   group: "edges", \
                   data: {{ \
                   source: "{e.source.label}", \
                   target: "{e.target.label}", \
                   }} \
                   }}"""

        return ",".join(map(parse, edges))

    def __parse_layers(self, layers: List[str]) -> str:
        def parse(layer: str):
            return f"""{{ \
                   group: "nodes", \
                   data: {{ \
                   id: "{layer}", \
                   layer_name: "{layer}", \
                   type: "layer", \
                   }} \
                   }}"""

        return ",".join(map(parse, layers))

    def __parse_nodes(self, nodes: List[Notebook]) -> str:
        def parse(n: Notebook):
            return f"""{{ \
                   group: "nodes", \
                   data: {{ \
                   id: "{n.label}", \
                   name: "{n.label.replace('/', '_')}", \
                   parent: "{n.layer}", \
                   notebookId: "{n.id}", \
                   type: "notebook", \
                   }} \
                   }}"""

        return ",".join(map(parse, nodes))
