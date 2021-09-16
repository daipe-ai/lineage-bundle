from lineagebundle.pipeline.NotebooksRelation import NotebooksRelation
from lineagebundle.pipeline.PipelinesEdgesPreparer import PipelinesEdgesPreparer
from lineagebundle.notebook.function.NotebookFunction import NotebookFunction
from typing import List


class PipelinesLineageGenerator:
    def __init__(self, pipelines_edges_preparer: PipelinesEdgesPreparer):
        self.__pipelines_edges_preparer = pipelines_edges_preparer

    def generate(self, entities) -> List[NotebooksRelation]:
        notebook_functions = (entity for entity in entities if isinstance(entity, NotebookFunction))
        nodes_with_tables = list(filter(lambda node: node.input_datasets != [] or node.output_dataset, notebook_functions))

        relations = self.__pipelines_edges_preparer.prepare(nodes_with_tables)

        return list(map(lambda relation: NotebooksRelation(*relation), relations))
