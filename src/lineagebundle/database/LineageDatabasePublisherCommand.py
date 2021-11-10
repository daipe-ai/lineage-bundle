from consolebundle.ConsoleCommand import ConsoleCommand

from lineagebundle.database.DatabasePublisher import DatabasePublisher
from logging import Logger


class LineageDatabasePublisherCommand(ConsoleCommand):
    def __init__(
        self,
        logger: Logger,
        database_publisher: DatabasePublisher,
    ):
        self.__logger = logger
        self.__database_publisher = database_publisher

    def get_command(self) -> str:
        return "lineage:publish:database"

    def get_description(self):
        return "Publishes lineage for all notebooks"

    def run(self, _):
        self.__logger.info("Listing notebooks")

        self.__logger.info("Publishing notebook DAGs")
        self.__logger.info("Publishing pipelines DAGs")

        self.__database_publisher.publish()

        self.__logger.info("All DAGs published")
