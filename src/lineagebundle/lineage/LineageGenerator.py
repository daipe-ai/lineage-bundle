from lineagebundle.notebook.NotebookCreationFacade import NotebookCreationFacade
from lineagebundle.notebook.NotebookFunctionsLineageGenerator import NotebookFunctionsLineageGenerator
from lineagebundle.notebook.NotebookList import NotebookList
from lineagebundle.notebook.NotebooksLocator import NotebooksLocator
from lineagebundle.notebook.function.NotebookFunction import NotebookFunction
from lineagebundle.notebook.function.NotebookFunctionsRelation import NotebookFunctionsRelation
from lineagebundle.pipeline.NotebooksRelation import NotebooksRelation
from lineagebundle.pipeline.PipelinesLineageGenerator import PipelinesLineageGenerator
from logging import Logger
from networkx import DiGraph
from sqlalchemybundle.entity.Base import Base
from typing import List, Tuple, Optional


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
        notebook_list = self.get_notebooks()

        notebook_functions, _ = self.__notebook_functions_lineage_generator.generate(notebook_list)
        return self.__pipelines_lineage_generator.get_graph(notebook_functions)

    def generate_entities(self) -> List[Base]:
        notebook_list = self.get_notebooks()

        notebook_functions, notebook_function_relations = self.get_notebook_function_relations(notebook_list)
        notebook_relations, _, _ = self.get_notebook_relations(notebook_list)

        return list(notebook_list) + notebook_relations + notebook_functions + notebook_function_relations

    def get_notebook_function_relations(self, notebook_list: NotebookList) -> Tuple[NotebookFunction, NotebookFunctionsRelation]:
        return self.__notebook_functions_lineage_generator.generate(notebook_list)

    def get_notebook_relations(self, notebook_list: NotebookList) -> List[NotebooksRelation]:
        notebook_functions, notebook_function_relations = self.get_notebook_function_relations(notebook_list)
        return self.__pipelines_lineage_generator.generate(notebook_functions), notebook_functions, notebook_function_relations

    def get_notebooks(self) -> Optional[NotebookList]:
        notebook_paths = self.__notebooks_locator.locate()

        if not notebook_paths:
            self.__logger.warning("No notebooks to process")
            return None

        return self.__notebook_creation_facade.create(notebook_paths)
