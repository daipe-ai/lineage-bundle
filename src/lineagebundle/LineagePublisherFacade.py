from typing import List, Dict, Any
from sqlalchemy.orm.session import Session
from lineagebundle.notebook.edge.LineageEdge import LineageEdge
from lineagebundle.notebook.node.LineageNode import LineageNode


class LineagePublisherFacade:
    def __init__(
        self,
        orm_session: Session,
    ):
        self.__orm_session = orm_session

    def publish(self, notebooks_with_nodes: List[Dict[str, Any]], notebooks_with_edges: List[Dict[str, Any]]):
        self.__orm_session.query(LineageNode).delete(synchronize_session=False)
        self.__orm_session.query(LineageEdge).delete(synchronize_session=False)

        entities = []

        for notebook_with_nodes in notebooks_with_nodes:
            for node in notebook_with_nodes["nodes"]:
                parsed_node = LineageNode(node.name, notebook_with_nodes["notebook"], node.input_table, node.output_table)
                entities.append(parsed_node)

        for notebook_with_edges in notebooks_with_edges:
            for edge in notebook_with_edges["edges"]:
                parsed_edge = LineageEdge(notebook_with_edges["notebook"], edge.source, edge.target)
                entities.append(parsed_edge)

        self.__orm_session.add_all(entities)
        self.__orm_session.commit()
