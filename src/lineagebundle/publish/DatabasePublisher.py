from datetime import datetime
from lineagebundle.notebook.function.NotebookFunction import NotebookFunction
from lineagebundle.notebook.function.NotebookFunctionsRelation import NotebookFunctionsRelation
from lineagebundle.pipeline.NotebooksRelation import NotebooksRelation
from lineagebundle.notebook.Notebook import Notebook
from sqlalchemybundle.session.SessionLazy import SessionLazy
from sqlalchemybundle.entity.Base import Base
from typing import List


class DatabasePublisher:
    def __init__(self, session_lazy: SessionLazy):
        self.__session_lazy = session_lazy

    def publish(self, entities: List[Base]):
        self.__delete_everything()

        orm_session = self.__session_lazy.get
        orm_session.add_all(entities)
        orm_session.commit()

    def __delete_everything(self):
        self.__delete(NotebookFunction)
        self.__delete(NotebookFunctionsRelation)
        self.__delete(NotebooksRelation)
        self.__delete(Notebook)
        self.__session_lazy.get.commit()

    def __delete(self, class_):
        self.__session_lazy.get.query(class_).update({"deleted_at": datetime.now()})
