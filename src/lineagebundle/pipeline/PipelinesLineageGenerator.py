from lineagebundle.notebook.function.NotebookFunction import NotebookFunction
from lineagebundle.pipeline.NotebooksRelation import NotebooksRelation
from lineagebundle.pipeline.PipelinesGraphPreparer import PipelinesGraphPreparer
from networkx import DiGraph
from typing import List


class PipelinesLineageGenerator:
    def __init__(self, pipelines_graph_preparer: PipelinesGraphPreparer):
        self.__pipelines_graph_preparer = pipelines_graph_preparer

    def get_graph(self, notebook_functions: List[NotebookFunction]) -> DiGraph:
        nodes_with_tables = list(filter(lambda node: node.input_datasets != [] or node.output_dataset, notebook_functions))

        return self.__pipelines_graph_preparer.prepare(nodes_with_tables)

    def generate(self, notebook_functions: List[NotebookFunction]) -> List[NotebooksRelation]:
        relations = self.get_graph(notebook_functions).edges
        return list(map(lambda relation: NotebooksRelation(*relation), relations))
