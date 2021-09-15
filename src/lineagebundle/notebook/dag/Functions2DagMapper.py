from lineagebundle.notebook.function.ParsedNotebookFunction import ParsedNotebookFunction
from lineagebundle.notebook.function.ParsedNotebookFunctionsRelation import ParsedNotebookFunctionsRelation
from typing import List, Tuple
from lineagebundle.notebook.decorator.Function import Function


class Functions2DagMapper:
    def map(self, results: List[Function]) -> Tuple[List[ParsedNotebookFunction], List[ParsedNotebookFunctionsRelation]]:
        nodes = []
        edges = []

        for result in results:
            nodes += result.get_nodes()
            edges += result.get_edges()

        return nodes, edges
