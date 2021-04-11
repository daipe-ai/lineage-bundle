from typing import List
from lineagebundle.notebook.node.LineageNode import LineageNode


class PipelinesEdgesPreparer:
    def prepare(self, nodes_with_tables: List[LineageNode]):
        unique_nodes = self.__get_unique_nodes(nodes_with_tables)
        output_table2notebook = self.__map_output_tables2_notebooks(nodes_with_tables)

        all_processed_tables = set()
        run_layers = []

        next_layer_notebooks = []
        current_tables = set()
        current_layer_notebooks = []

        edges = []

        while unique_nodes:
            unique_node = unique_nodes.pop(0)

            if unique_node["input_tables"] - all_processed_tables == set():
                current_layer_notebooks.append(unique_node)
                current_tables |= unique_node["output_tables"]
            else:
                next_layer_notebooks.append(unique_node)

            if not unique_nodes:
                for unique_node in current_layer_notebooks:
                    for input_table in unique_node["input_tables"]:
                        edges.append([output_table2notebook[input_table], unique_node["notebook"]])

                run_layers.append(current_layer_notebooks)
                current_layer_notebooks = []

                all_processed_tables |= current_tables
                current_tables = set()

                if next_layer_notebooks:
                    unique_nodes += next_layer_notebooks
                    next_layer_notebooks = []

        # return run_layers
        return edges

    def __get_unique_nodes(self, nodes_with_tables):
        notebooks2tables = dict()

        for node_with_table in nodes_with_tables:
            if node_with_table.notebook.id not in notebooks2tables:
                notebooks2tables[node_with_table.notebook.id] = {
                    "input_tables": set(),
                    "output_tables": set(),
                    "notebook": node_with_table.notebook,
                }

            if node_with_table.input_table:
                notebooks2tables[node_with_table.notebook.id]["input_tables"].add(node_with_table.input_table)

            if node_with_table.output_table:
                notebooks2tables[node_with_table.notebook.id]["output_tables"].add(node_with_table.output_table)

        return list(notebooks2tables.values())

    def __map_output_tables2_notebooks(self, nodes_with_tables):
        return {
            node_with_table.output_table: node_with_table.notebook for node_with_table in nodes_with_tables if node_with_table.output_table
        }
