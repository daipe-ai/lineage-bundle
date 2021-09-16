from consolebundle.ConsoleCommand import ConsoleCommand
from lineagebundle.LineageGenerator import LineageGenerator

from lineagebundle.publish.DatabasePublisher import DatabasePublisher
from logging import Logger


class LineageDBPublisherCommand(ConsoleCommand):
    def __init__(
        self,
        logger: Logger,
        database_publisher: DatabasePublisher,
        lineage_generator: LineageGenerator,
    ):
        self.__logger = logger
        self.__database_publisher = database_publisher
        self.__lineage_generator = lineage_generator

    def get_command(self) -> str:
        return "lineage:publish:database"

    def get_description(self):
        return "Publishes lineage for all notebooks"

    def run(self, _):
        self.__logger.info("Listing notebooks")

        entities = self.__lineage_generator.generate_entities()

        self.__logger.info("Publishing notebook DAGs")
        self.__logger.info("Publishing pipelines DAGs")

        self.__database_publisher.publish(entities)

        self.__logger.info("All DAGs published")
