from lineagebundle.notebook.NotebookCreationFacade import NotebookCreationFacade
from lineagebundle.notebook.NotebookFunctionsLineageGenerator import NotebookFunctionsLineageGenerator
from lineagebundle.notebook.NotebookList import NotebookList
from lineagebundle.notebook.NotebooksLocator import NotebooksLocator
from lineagebundle.pipeline.PipelinesLineageGenerator import PipelinesLineageGenerator
from logging import Logger
from networkx import DiGraph
from sqlalchemybundle.entity.Base import Base
from typing import List


class LineageGenerator:
    def __init__(
        self,
        logger: Logger,
        notebooks_locator: NotebooksLocator,
        notebook_creation_facade: NotebookCreationFacade,
        notebook_functions_lineage_generator: NotebookFunctionsLineageGenerator,
        pipelines_lineage_generator: PipelinesLineageGenerator,
    ):
        self.__logger = logger
        self.__notebooks_locator = notebooks_locator
        self.__notebook_creation_facade = notebook_creation_facade
        self.__notebook_functions_lineage_generator = notebook_functions_lineage_generator
        self.__pipelines_lineage_generator = pipelines_lineage_generator

    def get_pipelines_graph(self) -> DiGraph:
        notebook_list = self.__prepare_notebooks()

        functions_entities = self.__notebook_functions_lineage_generator.generate(notebook_list)
        return self.__pipelines_lineage_generator.get_graph(functions_entities)

    def generate_entities(self) -> List[Base]:
        notebook_list = self.__prepare_notebooks()

        functions_entities, pipelines_entities = self.get_notebook_relations(notebook_list)

        return list(notebook_list) + functions_entities + pipelines_entities

    def get_notebook_relations(self, notebook_list: NotebookList):
        functions_entities = self.__notebook_functions_lineage_generator.generate(notebook_list)
        return functions_entities, self.__pipelines_lineage_generator.generate(functions_entities)

    def __prepare_notebooks(self):
        notebook_paths = self.__notebooks_locator.locate()

        if not notebook_paths:
            self.__logger.warning("No notebooks to process")
            return

        return self.__notebook_creation_facade.create(notebook_paths)
