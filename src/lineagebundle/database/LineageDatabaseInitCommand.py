from logging import Logger

from consolebundle.ConsoleCommand import ConsoleCommand
from sqlalchemybundle.session.SessionLazy import SessionLazy
from sqlalchemybundle.entity.Base import Base


class LineageDatabaseInitCommand(ConsoleCommand):
    def __init__(
        self,
        logger: Logger,
        session_lazy: SessionLazy,
    ):
        self.__logger = logger
        self.__session_lazy = session_lazy

    def get_command(self) -> str:
        return "lineage:database:init"

    def get_description(self):
        return "Creates tables for lineage in a database"

    def run(self, _):
        self.__logger.info("Initializing database...")

        Base.metadata.create_all(self.__session_lazy.get.get_bind())

        self.__logger.info("Database successfully initialized.")
