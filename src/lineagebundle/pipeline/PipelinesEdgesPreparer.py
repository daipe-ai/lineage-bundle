from networkx.classes.reportviews import OutEdgeView
from typing import List
from lineagebundle.notebook.function.NotebookFunction import NotebookFunction
from networkx import DiGraph


class PipelinesEdgesPreparer:
    def prepare(self, nodes_with_tables: List[NotebookFunction]) -> OutEdgeView:
        unique_nodes = self.__get_unique_nodes(nodes_with_tables)
        graph = DiGraph()

        all_nodes = unique_nodes.copy()
        while unique_nodes:
            unique_node = unique_nodes.pop(0)

            for other_node in all_nodes:
                if unique_node["input_tables"].intersection(other_node["output_tables"]):
                    graph.add_edge(other_node["notebook"], unique_node["notebook"])

        return graph.edges

    def __get_unique_nodes(self, nodes_with_tables):
        notebooks2tables = dict()

        for node_with_table in nodes_with_tables:
            if node_with_table.notebook.path not in notebooks2tables:
                notebooks2tables[node_with_table.notebook.path] = {
                    "input_tables": set(),
                    "output_tables": set(),
                    "notebook": node_with_table.notebook,
                }

            if node_with_table.input_datasets:
                for input_table in node_with_table.input_datasets:
                    notebooks2tables[node_with_table.notebook.path]["input_tables"].add(input_table)

            if node_with_table.output_dataset:
                notebooks2tables[node_with_table.notebook.path]["output_tables"].add(node_with_table.output_dataset)

        return list(notebooks2tables.values())
