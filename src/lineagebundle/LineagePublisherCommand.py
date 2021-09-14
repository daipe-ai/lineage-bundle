from argparse import Namespace
from lineagebundle.pipeline.NotebooksRelation import NotebooksRelation
from lineagebundle.publisher.PublisherInterface import PublisherInterface
from logging import Logger
from pathlib import Path
from consolebundle.ConsoleCommand import ConsoleCommand
from lineagebundle.notebook.NotebookFunctionsFacade import NotebookFunctionsFacade
from lineagebundle.notebook.NotebookCreationFacade import NotebookCreationFacade
from lineagebundle.notebook.NotebooksLocator import NotebooksLocator
from lineagebundle.notebook.dag.DagCreator import DagCreator
from lineagebundle.notebook.NotebookList import NotebookList
from lineagebundle.pipeline.PipelinesLineageGenerator import PipelinesLineageGenerator
from sqlalchemy.orm.session import Session
from sqlalchemybundle.entity.Base import Base


class LineagePublisherCommand(ConsoleCommand):
    def __init__(
        self,
        root_module_path: str,
        logger: Logger,
        publisher: PublisherInterface,
        notebooks_locator: NotebooksLocator,
        notebook_creation_facade: NotebookCreationFacade,
        notebook_functions_facade: NotebookFunctionsFacade,
        dag_creator: DagCreator,
        pipelines_lineage_generator: PipelinesLineageGenerator,
        orm_session: Session,
    ):
        self.__root_module_path = Path(root_module_path)
        self.__logger = logger
        self.__publisher = publisher
        self.__notebooks_locator = notebooks_locator
        self.__notebook_creation_facade = notebook_creation_facade
        self.__notebook_functions_facade = notebook_functions_facade
        self.__dag_creator = dag_creator
        self.__pipelines_lineage_generator = pipelines_lineage_generator
        self.__orm_session = orm_session

    def get_command(self) -> str:
        return "lineage:publish"

    def get_description(self):
        return "Publishes lineage for all notebooks"

    def run(self, input_args: Namespace):
        self.__logger.info("Listing notebooks")

        Base.metadata.create_all(self.__orm_session.get_bind())

        notebook_list = self.__prepare_notebooks()
        entities = self.__prepare_entities(notebook_list)

        self.__logger.info("Publishing notebook DAGs")
        self.__logger.info("Publishing pipelines DAGs")

        self.__publisher.publish(entities)

        self.__logger.info("All DAGs published")

    def __prepare_entities(self, notebook_list):
        notebooks_with_nodes, notebooks_with_edges = self.__get_notebooks_lineage(notebook_list)
        entities = self.__notebook_functions_facade.prepare(notebooks_with_nodes, notebooks_with_edges)

        relations = self.__pipelines_lineage_generator.generate(entities)
        entities.extend(NotebooksRelation(*relation) for relation in relations)
        return entities

    def __prepare_notebooks(self):
        notebook_paths = self.__notebooks_locator.locate()

        if not notebook_paths:
            self.__logger.warning("No notebooks to process")
            return

        return self.__notebook_creation_facade.create(notebook_paths)

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
