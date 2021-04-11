from typing import List
from lineagebundle.notebook.decorator.Function import Function


class Functions2DagMapper:
    def map(self, results: List[Function]):
        nodes = []
        edges = []

        for result in results:
            nodes += result.get_nodes()
            edges += result.get_edges()

        return nodes, edges
