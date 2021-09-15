from consolebundle.ConsoleCommand import ConsoleCommand
from lineagebundle.LineageGenerator import LineageGenerator
from lineagebundle.notebook.NotebookCreationFacade import NotebookCreationFacade
from lineagebundle.notebook.NotebooksLocator import NotebooksLocator
from lineagebundle.publisher.PublisherInterface import PublisherInterface
from logging import Logger


class LineagePublisherCommand(ConsoleCommand):
    def __init__(
        self,
        logger: Logger,
        publisher: PublisherInterface,
        notebooks_locator: NotebooksLocator,
        notebook_creation_facade: NotebookCreationFacade,
        lineage_generator: LineageGenerator,
    ):
        self.__logger = logger
        self.__publisher = publisher
        self.__notebooks_locator = notebooks_locator
        self.__notebook_creation_facade = notebook_creation_facade
        self.__lineage_generator = lineage_generator

    def get_command(self) -> str:
        return "lineage:publish"

    def get_description(self):
        return "Publishes lineage for all notebooks"

    def run(self, _):
        self.__logger.info("Listing notebooks")

        notebook_list = self.__prepare_notebooks()
        entities = self.__lineage_generator.generate_entities(notebook_list)

        self.__logger.info("Publishing notebook DAGs")
        self.__logger.info("Publishing pipelines DAGs")

        self.__publisher.publish(entities)

        self.__logger.info("All DAGs published")

    def __prepare_notebooks(self):
        notebook_paths = self.__notebooks_locator.locate()

        if not notebook_paths:
            self.__logger.warning("No notebooks to process")
            return

        return self.__notebook_creation_facade.create(notebook_paths)
