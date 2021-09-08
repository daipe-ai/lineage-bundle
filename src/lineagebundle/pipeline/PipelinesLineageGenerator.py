from sqlalchemy.orm.session import Session
from lineagebundle.pipeline.PipelinesEdgesPreparer import PipelinesEdgesPreparer
from lineagebundle.notebook.function.NotebookFunction import NotebookFunction


class PipelinesLineageGenerator:
    def __init__(self, orm_session: Session, pipelines_edges_preparer: PipelinesEdgesPreparer):
        self.__orm_session = orm_session
        self.__pipelines_edges_preparer = pipelines_edges_preparer

    def generate(self, entities):
        notebook_functions = [entity for entity in entities if isinstance(entity, NotebookFunction)]
        nodes_with_tables = list(filter(lambda node: node.input_datasets != [] or node.output_dataset, notebook_functions))

        relations = self.__pipelines_edges_preparer.prepare(nodes_with_tables)

        return relations
