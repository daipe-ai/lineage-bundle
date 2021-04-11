from pathlib import Path
from lineagebundle.notebook.NotebookParser import NotebookParser
from lineagebundle.notebook.dag.Functions2DagMapper import Functions2DagMapper


class DagCreator:
    def __init__(self, notebook_parser: NotebookParser, functions2dag_mapper: Functions2DagMapper):
        self.__notebook_parser = notebook_parser
        self.__functions2dag_mapper = functions2dag_mapper

    def create(self, notebook_path: Path):
        results = self.__notebook_parser.parse(notebook_path)

        return self.__functions2dag_mapper.map(results)
