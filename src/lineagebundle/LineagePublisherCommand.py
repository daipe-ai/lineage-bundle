from argparse import Namespace
from lineagebundle.notebook.Notebook import Notebook
from lineagebundle.notebook.function.NotebookFunction import NotebookFunction
from lineagebundle.notebook.function.NotebookFunctionsRelation import NotebookFunctionsRelation
from lineagebundle.pipeline.NotebooksRelation import NotebooksRelation
from logging import Logger
from pathlib import Path
from consolebundle.ConsoleCommand import ConsoleCommand
from lineagebundle.LineagePublisherFacade import LineagePublisherFacade
from lineagebundle.notebook.NotebookCreationFacade import NotebookCreationFacade
from lineagebundle.notebook.NotebooksLocator import NotebooksLocator
from lineagebundle.notebook.dag.DagCreator import DagCreator
from lineagebundle.notebook.NotebookList import NotebookList
from lineagebundle.pipeline.PipelinesLineageGenerator import PipelinesLineageGenerator
from sqlalchemy.orm.session import Session


class LineagePublisherCommand(ConsoleCommand):
    def __init__(
        self,
        root_module_path: str,
        logger: Logger,
        notebooks_locator: NotebooksLocator,
        notebook_creation_facade: NotebookCreationFacade,
        dag_creator: DagCreator,
        lineage_publisher_facade: LineagePublisherFacade,
        pipelines_lineage_generator: PipelinesLineageGenerator,
        orm_session: Session,
    ):
        self.__root_module_path = Path(root_module_path)
        self.__logger = logger
        self.__notebooks_locator = notebooks_locator
        self.__notebook_creation_facade = notebook_creation_facade
        self.__dag_creator = dag_creator
        self.__lineage_publisher_facade = lineage_publisher_facade
        self.__pipelines_lineage_generator = pipelines_lineage_generator
        self.__orm_session = orm_session

    def get_command(self) -> str:
        return "lineage:publish"

    def get_description(self):
        return "Publishes lineage for all notebooks"

    def run(self, input_args: Namespace):
        self.__logger.info("Listing notebooks")

        notebook_list = self.__prepare_notebooks()

        self.__logger.info("Publishing notebook DAGs")

        entities = self.__publish_notebooks_lineage(notebook_list)

        self.__logger.info("Publishing pipelines DAGs")

        relations = self.__pipelines_lineage_generator.generate(entities)

        self.__publish_all(entities, relations)

        self.__logger.info("All DAGs published")

    def __publish_all(self, entities, relations):
        self.__orm_session.query(NotebookFunction).delete(synchronize_session=False)
        self.__orm_session.query(NotebookFunctionsRelation).delete(synchronize_session=False)
        self.__orm_session.query(NotebooksRelation).delete(synchronize_session=False)
        self.__orm_session.query(Notebook).delete(synchronize_session=False)

        self.__orm_session.add_all(entities)
        self.__orm_session.add_all([NotebooksRelation(relation[0], relation[1]) for relation in relations])

        self.__orm_session.commit()

    def __prepare_notebooks(self):
        notebook_paths = self.__notebooks_locator.locate()

        if not notebook_paths:
            self.__logger.warning("No notebooks to process")
            return

        return self.__notebook_creation_facade.create(notebook_paths)

    def __publish_notebooks_lineage(self, notebook_list: NotebookList):
        notebooks_with_nodes, notebooks_with_edges = self.__get_notebooks_lineage(notebook_list)

        return self.__lineage_publisher_facade.publish(notebooks_with_nodes, notebooks_with_edges)

    def __get_notebooks_lineage(self, notebook_list: NotebookList):
        notebooks_with_nodes = []
        notebooks_with_edges = []

        for notebook in notebook_list:
            notebook_path = self.__root_module_path.parent.joinpath(notebook.path)
            nodes, edges = self.__dag_creator.create(notebook_path)

            notebooks_with_nodes.append({"notebook": notebook, "nodes": nodes})
            notebooks_with_edges.append({"notebook": notebook, "edges": edges})

        return notebooks_with_nodes, notebooks_with_edges
