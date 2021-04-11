from datetime import datetime
from pathlib import Path
from typing import List
from lineagebundle.notebook.LayerResolver import LayerResolver
from sqlalchemy.orm.session import Session
from lineagebundle.pipeline.Notebook import Notebook
from lineagebundle.pipeline.NotebookList import NotebookList


class NotebookCreationFacade:
    def __init__(
        self,
        orm_session: Session,
        layer_resolver: LayerResolver,
    ):
        self.__orm_session = orm_session
        self.__layer_resolver = layer_resolver

    def create(self, notebook_paths: List[Path]):
        existing_notebook_list = self.__find_existing_notebooks(notebook_paths)

        notebooks = [self.__create_notebook(notebook_path, existing_notebook_list) for notebook_path in notebook_paths]
        deleted_notebooks = self.__get_deleted_notebooks(notebook_paths)

        self.__orm_session.add_all(notebooks)
        self.__orm_session.add_all(deleted_notebooks)
        self.__orm_session.commit()

        return NotebookList(notebooks)

    def __find_existing_notebooks(self, notebook_paths: List[Path]):
        notebook_paths_str = [str(notebook_path.as_posix()) for notebook_path in notebook_paths]
        notebooks = self.__orm_session.query(Notebook).filter(
            Notebook.path.in_(notebook_paths_str),
            Notebook.deleted_at.is_(None),
        )

        return NotebookList(notebooks)

    def __create_notebook(self, notebook_path: Path, existing_notebook_list: NotebookList):
        notebook_path_str = str(notebook_path.as_posix())
        label = notebook_path.parent.parent.stem + "/" + notebook_path.stem

        existing_notebook: Notebook = existing_notebook_list.find(lambda notebook: notebook.path == notebook_path_str)

        if existing_notebook:
            existing_notebook.update(label, self.__layer_resolver.resolve(notebook_path_str))

            return existing_notebook

        return Notebook(label, notebook_path_str, self.__layer_resolver.resolve(notebook_path_str))

    def __get_deleted_notebooks(self, notebook_paths: List[Path]):
        notebook_paths_str = [str(notebook_path.as_posix()) for notebook_path in notebook_paths]
        notebooks = self.__orm_session.query(Notebook).filter(
            Notebook.path.notin_(notebook_paths_str),
            Notebook.deleted_at.is_(None),
        )

        for notebook in notebooks:
            notebook.deleted_at = datetime.now()

        return notebooks
