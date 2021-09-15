from lineagebundle.notebook.NotebookFunctionsLineageGenerator import NotebookFunctionsLineageGenerator
from lineagebundle.notebook.NotebookList import NotebookList
from lineagebundle.pipeline.PipelinesLineageGenerator import PipelinesLineageGenerator
from sqlalchemybundle.entity.Base import Base
from typing import List


class LineageGenerator:
    def __init__(
        self,
        notebook_functions_lineage_generator: NotebookFunctionsLineageGenerator,
        pipelines_lineage_generator: PipelinesLineageGenerator,
    ):
        self.__notebook_functions_lineage_generator = notebook_functions_lineage_generator
        self.__pipelines_lineage_generator = pipelines_lineage_generator

    def generate_entities(self, notebook_list: NotebookList) -> List[Base]:
        functions_entities = self.__notebook_functions_lineage_generator.generate(notebook_list)
        pipelines_entities = self.__pipelines_lineage_generator.generate(functions_entities)

        return functions_entities + pipelines_entities
