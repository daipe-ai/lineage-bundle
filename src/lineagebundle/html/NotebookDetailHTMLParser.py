import os
from lineagebundle.notebook.function.NotebookFunction import NotebookFunction
from lineagebundle.notebook.function.NotebookFunctionsRelation import NotebookFunctionsRelation
from typing import List


class NotebookDetailHTMLParser:
    def parse(self, notebook_functions: List[NotebookFunction], notebook_functions_relations: List[NotebookFunctionsRelation]) -> str:
        template_path = os.path.join(os.path.dirname(__file__), "templates/template.html")
        with open(template_path) as html_file:
            html = html_file.read()

        return html.replace("NODES_PLACEHOLDER", self.__parse_notebook_functions(notebook_functions)).replace(
            "EDGES_PLACEHOLDER", self.__parse_function_edges(notebook_functions_relations)
        )

    def __parse_function_edges(self, edges: List[NotebookFunctionsRelation]) -> str:
        def parse(e: NotebookFunctionsRelation):
            return f"""{{ \
                   group: "edges", \
                   data: {{ \
                   source: "{e.source}", \
                   target: "{e.target}", \
                   }} \
                   }}"""

        return ",".join(map(parse, edges))

    def __parse_notebook_functions(self, notebook_functions: List[NotebookFunction]) -> str:
        def parse(n: NotebookFunction):
            return f"""{{ \
                   group: "nodes", \
                   data: {{ \
                   id: "{n.name}", \
                   type: "{"inputDataset" if n.input_datasets else ("outputDataset" if n.output_dataset else "function")}", \
                   }} \
                   }}"""

        return ",".join(map(parse, notebook_functions))
