from pathlib import Path
from typing import List
from lineagebundle.notebook.LayerResolver import LayerResolver
from lineagebundle.notebook.Notebook import Notebook
from lineagebundle.notebook.NotebookList import NotebookList


class NotebookCreationFacade:
    def __init__(
        self,
        layer_resolver: LayerResolver,
    ):
        self.__layer_resolver = layer_resolver

    def create(self, notebook_paths: List[Path]) -> NotebookList:
        notebooks = [self.__create_notebook(notebook_path) for notebook_path in notebook_paths]

        return NotebookList(notebooks)

    def __create_notebook(self, notebook_path: Path) -> Notebook:
        notebook_path_str = str(notebook_path.as_posix())

        if notebook_path.stem != notebook_path.parent.stem:
            label = notebook_path.parent.stem + "/" + notebook_path.stem
        else:
            label = notebook_path.parent.parent.stem + "/" + notebook_path.parent.stem

        return Notebook(label, notebook_path_str, self.__layer_resolver.resolve(notebook_path_str))
