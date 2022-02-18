import os
from lineagebundle.notebook.Notebook import Notebook
from lineagebundle.notebook.function.NotebookFunctionsRelation import NotebookFunctionsRelation
from lineagebundle.pipeline.NotebooksRelation import NotebooksRelation
from logging import Logger
from pathlib import Path
from typing import List, Union


class PipelinesHTMLParser:
    def __init__(self, logger: Logger, notebooks_subpath: str):
        self.__logger = logger
        self.__notebooks_subpath = Path(notebooks_subpath)

    def parse(
        self,
        layers: List[str],
        notebooks: List[Notebook],
        edges: List[Union[NotebooksRelation, NotebookFunctionsRelation]],
        on_tap_enabled: bool,
    ) -> str:
        template_path = os.path.join(os.path.dirname(__file__), "templates/template.html")
        with open(template_path, encoding="utf-8") as html_file:
            html = html_file.read()

        if on_tap_enabled:
            html = html.replace(
                "ON_TAP_LISTENER", self.__on_tap_listener(f"'{self.__notebooks_subpath}/' + e.target" f".data('name') + '.html'")
            )
        else:
            html = html.replace("ON_TAP_LISTENER", "")

        html = html.replace("NODES_PLACEHOLDER", self.__parse_nodes(notebooks) + "," + self.__parse_layers(layers)).replace(
            "EDGES_PLACEHOLDER", self.__parse_edges(edges)
        )

        try:
            from minify_html import minify  # pylint: disable = import-outside-toplevel # pyre-ignore[21]

            self.__logger.info("minify_html is installed. Writing minified html code.")
            return minify(html, minify_css=True, minify_js=True)
        except ImportError:
            self.__logger.info("minify_html is NOT installed. Writing non minified html code.")
            return html

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

    def __on_tap_listener(self, href: str):
        return """
            cy.on('tap', 'node[type = "notebook"]', (e) => {
                document.location.href = HREF_PLACEHOLDER
            });
            """.replace(
            "HREF_PLACEHOLDER", href
        )
