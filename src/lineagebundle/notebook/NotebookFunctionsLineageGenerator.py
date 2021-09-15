from lineagebundle.notebook.NotebookList import NotebookList
from lineagebundle.notebook.dag.DagCreator import DagCreator

from lineagebundle.notebook.function.NotebookFunctionsRelation import NotebookFunctionsRelation
from lineagebundle.notebook.function.NotebookFunction import NotebookFunction
from pathlib import Path
from typing import List, Union


class NotebookFunctionsLineageGenerator:
    def __init__(
        self,
        root_module_path: str,
        dag_creator: DagCreator,
    ):
        self.__root_module_path = Path(root_module_path)
        self.__dag_creator = dag_creator

    def generate(self, notebook_list: NotebookList) -> List[Union[NotebookFunction, NotebookFunctionsRelation]]:
        notebooks_with_nodes, notebooks_with_edges = self.__get_notebooks_lineage(notebook_list)
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

    def __get_notebooks_lineage(self, notebook_list: NotebookList):
        notebooks_with_nodes = []
        notebooks_with_edges = []

        for notebook in notebook_list:
            notebook_path = self.__root_module_path.parent.joinpath(notebook.path)
            nodes, edges = self.__dag_creator.create(notebook_path)

            notebooks_with_nodes.append({"notebook": notebook, "nodes": nodes})

            output_tables = [node for node in nodes if node.output_table]
            if len(output_tables) > 1:
                raise Exception(
                    f"Notebook {notebook.label} outputs more than one table in functions: {', '.join(map(lambda node: node.name, output_tables))}"
                )

            notebooks_with_edges.append({"notebook": notebook, "edges": edges})

        return notebooks_with_nodes, notebooks_with_edges
