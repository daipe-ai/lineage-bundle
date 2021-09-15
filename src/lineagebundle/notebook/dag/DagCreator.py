from lineagebundle.notebook.function.ParsedNotebookFunction import ParsedNotebookFunction
from lineagebundle.notebook.function.ParsedNotebookFunctionsRelation import ParsedNotebookFunctionsRelation
from pathlib import Path
from lineagebundle.notebook.NotebookParser import NotebookParser
from lineagebundle.notebook.dag.Functions2DagMapper import Functions2DagMapper
from typing import Tuple, List


class DagCreator:
    def __init__(self, notebook_parser: NotebookParser, functions2dag_mapper: Functions2DagMapper):
        self.__notebook_parser = notebook_parser
        self.__functions2dag_mapper = functions2dag_mapper

    def create(self, notebook_path: Path) -> Tuple[List[ParsedNotebookFunction], List[ParsedNotebookFunctionsRelation]]:
        results = self.__notebook_parser.parse(notebook_path)

        return self.__functions2dag_mapper.map(results)
