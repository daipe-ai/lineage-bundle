from typing import List, Dict, Any

from lineagebundle.notebook.function.NotebookFunctionsRelation import NotebookFunctionsRelation
from lineagebundle.notebook.function.NotebookFunction import NotebookFunction


class LineagePublisherFacade:
    def publish(self, notebooks_with_nodes: List[Dict[str, Any]], notebooks_with_edges: List[Dict[str, Any]]):

        entities = []

        for notebook_with_nodes in notebooks_with_nodes:
            for node in notebook_with_nodes["nodes"]:
                parsed_node = NotebookFunction(node.name, notebook_with_nodes["notebook"], node.input_tables, node.output_table)
                entities.append(parsed_node)

        for notebook_with_edges in notebooks_with_edges:
            for edge in notebook_with_edges["edges"]:
                parsed_edge = NotebookFunctionsRelation(notebook_with_edges["notebook"], edge.source, edge.target)
                entities.append(parsed_edge)

        return entities
