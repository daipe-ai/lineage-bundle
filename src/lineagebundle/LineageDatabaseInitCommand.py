from logging import Logger

from consolebundle.ConsoleCommand import ConsoleCommand
from sqlalchemy.orm.session import Session
from sqlalchemybundle.entity.Base import Base


class LineageDatabaseInitCommand(ConsoleCommand):
    def __init__(
        self,
        logger: Logger,
        orm_session: Session,
    ):
        self.__logger = logger
        self.__orm_session = orm_session

    def get_command(self) -> str:
        return "lineage:database:init"

    def get_description(self):
        return "Creates tables for lineage in a database"

    def run(self, _):
        self.__logger.info("Initializing database...")

        Base.metadata.create_all(self.__orm_session.get_bind())

        self.__logger.info("Database successfully initialized.")
