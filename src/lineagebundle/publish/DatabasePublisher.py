from datetime import datetime
from lineagebundle.notebook.function.NotebookFunction import NotebookFunction
from lineagebundle.notebook.function.NotebookFunctionsRelation import NotebookFunctionsRelation
from lineagebundle.pipeline.NotebooksRelation import NotebooksRelation
from lineagebundle.notebook.Notebook import Notebook
from sqlalchemy.orm.session import Session
from sqlalchemybundle.entity.Base import Base
from typing import List


class DatabasePublisher:
    def __init__(self, orm_session: Session):
        self.__orm_session = orm_session

    def publish(self, entities: List[Base]):
        self.__delete_everything()

        self.__orm_session.add_all(entities)
        self.__orm_session.commit()

    def __delete_everything(self):
        self.__delete(NotebookFunction)
        self.__delete(NotebookFunctionsRelation)
        self.__delete(NotebooksRelation)
        self.__delete(Notebook)
        self.__orm_session.commit()

    def __delete(self, class_):
        self.__orm_session.query(class_).update({"deleted_at": datetime.now()})
