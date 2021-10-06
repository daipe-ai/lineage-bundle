from datetime import datetime
from lineagebundle.lineage.LineageGenerator import LineageGenerator
from lineagebundle.notebook.Notebook import Notebook
from lineagebundle.notebook.function.NotebookFunction import NotebookFunction
from lineagebundle.notebook.function.NotebookFunctionsRelation import NotebookFunctionsRelation
from lineagebundle.pipeline.NotebooksRelation import NotebooksRelation
from sqlalchemybundle.session.SessionLazy import SessionLazy


class DatabasePublisher:
    def __init__(self, session_lazy: SessionLazy, lineage_generator: LineageGenerator):
        self.__session_lazy = session_lazy
        self.__lineage_generator = lineage_generator

    def publish(self):
        self.__delete_everything()

        orm_session = self.__session_lazy.get
        orm_session.add_all(self.__lineage_generator.all_entities)
        orm_session.commit()

    def __delete_everything(self):
        self.__delete(NotebookFunction)
        self.__delete(NotebookFunctionsRelation)
        self.__delete(NotebooksRelation)
        self.__delete(Notebook)
        self.__session_lazy.get.commit()

    def __delete(self, class_):
        self.__session_lazy.get.query(class_).update({"deleted_at": datetime.now()})
