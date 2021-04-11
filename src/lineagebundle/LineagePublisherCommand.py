from argparse import Namespace
from logging import Logger
from pathlib import Path
from consolebundle.ConsoleCommand import ConsoleCommand
from lineagebundle.LineagePublisherFacade import LineagePublisherFacade
from lineagebundle.notebook.NotebookCreationFacade import NotebookCreationFacade
from lineagebundle.notebook.NotebooksLocator import NotebooksLocator
from lineagebundle.notebook.dag.DagCreator import DagCreator
from lineagebundle.pipeline.NotebookList import NotebookList
from lineagebundle.pipeline.PipelinesLineageGenerator import PipelinesLineageGenerator


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
    ):
        self.__root_module_path = Path(root_module_path)
        self.__logger = logger
        self.__notebooks_locator = notebooks_locator
        self.__notebook_creation_facade = notebook_creation_facade
        self.__dag_creator = dag_creator
        self.__lineage_publisher_facade = lineage_publisher_facade
        self.__pipelines_lineage_generator = pipelines_lineage_generator

    def get_command(self) -> str:
        return "lineage:publish"

    def get_description(self):
        return "Publishes lineage for all notebooks"

    def run(self, input_args: Namespace):
        self.__logger.info("Listing notebooks")

        notebook_list = self.__prepare_notebooks()

        self.__logger.info("Publishing notebook DAGs")

        self.__publish_notebooks_lineage(notebook_list)

        self.__logger.info("Publishing pipelines DAGs")

        self.__pipelines_lineage_generator.generate()

        self.__logger.info("All DAGs published")

    def __prepare_notebooks(self):
        notebook_paths = self.__notebooks_locator.locate()
        return self.__notebook_creation_facade.create(notebook_paths)

    def __publish_notebooks_lineage(self, notebook_list: NotebookList):
        notebooks_with_nodes, notebooks_with_edges = self.__get_notebooks_lineage(notebook_list)

        self.__lineage_publisher_facade.publish(notebooks_with_nodes, notebooks_with_edges)

    def __get_notebooks_lineage(self, notebook_list: NotebookList):
        notebooks_with_nodes = []
        notebooks_with_edges = []

        for notebook in notebook_list:
            notebook_path = self.__root_module_path.parent.joinpath(notebook.path)
            nodes, edges = self.__dag_creator.create(notebook_path)

            notebooks_with_nodes.append({"notebook": notebook, "nodes": nodes})
            notebooks_with_edges.append({"notebook": notebook, "edges": edges})

        return notebooks_with_nodes, notebooks_with_edges
