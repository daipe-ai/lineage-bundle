from lineagebundle.notebook.Notebook import Notebook
from lineagebundle.notebook.dag.DagCreator import DagCreator
from lineagebundle.notebook.function.NotebookFunction import NotebookFunction
from lineagebundle.notebook.function.NotebookFunctionsRelation import NotebookFunctionsRelation
from pathlib import Path
from typing import Tuple, List


class NotebookFunctionsLineageGenerator:
    def __init__(
        self,
        root_module_path: str,
        dag_creator: DagCreator,
    ):
        self.__root_module_path = Path(root_module_path)
        self.__dag_creator = dag_creator

    def generate(self, notebooks: List[Notebook]) -> Tuple[List[NotebookFunction], List[NotebookFunctionsRelation]]:
        notebooks_with_nodes, notebooks_with_edges = self.__get_notebooks_lineage(notebooks)

        notebook_functions = []
        for notebook_with_nodes in notebooks_with_nodes:
            for node in notebook_with_nodes["nodes"]:
                parsed_node = NotebookFunction(node.name, notebook_with_nodes["notebook"], node.input_tables, node.output_table)
                notebook_functions.append(parsed_node)

        notebook_function_relations: List[NotebookFunctionsRelation] = []
        for notebook_with_edges in notebooks_with_edges:
            for edge in notebook_with_edges["edges"]:
                parsed_edge = NotebookFunctionsRelation(notebook_with_edges["notebook"], edge.source, edge.target)
                notebook_function_relations.append(parsed_edge)

        return notebook_functions, notebook_function_relations

    def __get_notebooks_lineage(self, notebooks: List[Notebook]):
        notebooks_with_nodes = []
        notebooks_with_edges = []

        for notebook in notebooks:
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
