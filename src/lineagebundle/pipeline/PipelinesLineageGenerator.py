from typing import List
from sqlalchemy.sql import expression
from sqlalchemy.orm.session import Session
from lineagebundle.pipeline.NotebooksRelation import NotebooksRelation
from lineagebundle.pipeline.PipelinesEdgesPreparer import PipelinesEdgesPreparer
from lineagebundle.notebook.node.LineageNode import LineageNode


class PipelinesLineageGenerator:
    def __init__(self, orm_session: Session, pipelines_edges_preparer: PipelinesEdgesPreparer):
        self.__orm_session = orm_session
        self.__pipelines_edges_preparer = pipelines_edges_preparer

    def generate(self):
        nodes_with_tables: List[LineageNode] = (
            self.__orm_session.query(LineageNode)
            .filter(
                expression.or_(LineageNode.input_table.isnot(None), LineageNode.output_table.isnot(None)),
            )
            .all()
        )

        relations = self.__pipelines_edges_preparer.prepare(nodes_with_tables)

        self.__orm_session.query(NotebooksRelation).delete(synchronize_session=False)

        self.__orm_session.add_all([NotebooksRelation(relation[0], relation[1]) for relation in relations])
        self.__orm_session.commit()
