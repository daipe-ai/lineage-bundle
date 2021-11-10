from lineagebundle.notebook.Notebook import Notebook
from lineagebundle.notebook.NotebookCreationFacade import NotebookCreationFacade
from lineagebundle.notebook.NotebookFunctionsLineageGenerator import NotebookFunctionsLineageGenerator
from lineagebundle.notebook.NotebooksLocator import NotebooksLocator
from lineagebundle.notebook.function.NotebookFunction import NotebookFunction
from lineagebundle.notebook.function.NotebookFunctionsRelation import NotebookFunctionsRelation
from lineagebundle.pipeline.NotebooksRelation import NotebooksRelation
from lineagebundle.pipeline.PipelinesLineageGenerator import PipelinesLineageGenerator
from logging import Logger
from networkx import DiGraph
from sqlalchemybundle.entity.Base import Base
from typing import List, Tuple
from werkzeug.utils import cached_property


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

    @cached_property
    def notebooks(self) -> List[Notebook]:
        notebook_paths = self.__notebooks_locator.locate()

        if not notebook_paths:
            self.__logger.warning("No notebooks to process")
            return []

        return self.__notebook_creation_facade.create(notebook_paths)

    @cached_property
    def notebooks_relations(self) -> List[NotebooksRelation]:
        return self.__pipelines_lineage_generator.generate(self.notebook_functions)

    @cached_property
    def notebook_functions_and_relations(self) -> Tuple[NotebookFunction, NotebookFunctionsRelation]:
        return self.__notebook_functions_lineage_generator.generate(self.notebooks)

    @cached_property
    def notebook_functions(self) -> List[NotebookFunction]:
        return self.notebook_functions_and_relations[0]

    @cached_property
    def notebook_functions_relations(self) -> List[NotebookFunctionsRelation]:
        return self.notebook_functions_and_relations[1]

    @cached_property
    def pipelines_graph(self) -> DiGraph:
        return self.__pipelines_lineage_generator.get_graph(self.notebook_functions)

    @cached_property
    def all_entities(self) -> List[Base]:
        return self.notebooks + self.notebooks_relations + self.notebook_functions + self.notebook_functions_relations
