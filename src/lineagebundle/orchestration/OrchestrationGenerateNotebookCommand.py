from consolebundle.ConsoleCommand import ConsoleCommand
from lineagebundle.lineage.LineageGenerator import LineageGenerator
from lineagebundle.orchestration.OrchestrationNotebookGenerator import OrchestrationNotebookGenerator
from logging import Logger
from networkx import topological_sort


class OrchestrationGenerateNotebookCommand(ConsoleCommand):
    def __init__(
        self,
        logger: Logger,
        lineage_generator: LineageGenerator,
        orchestration_notebook_generator: OrchestrationNotebookGenerator,
    ):
        self.__logger = logger
        self.__lineage_generator = lineage_generator
        self.__orchestration_notebook_generator = orchestration_notebook_generator

    def get_command(self) -> str:
        return "orchestration:generate:notebook"

    def get_description(self):
        return "Generates an orchestration notebook of all notebooks in a project"

    def run(self, _):
        self.__logger.info("Generating orchestration notebook...")
        graph = self.__lineage_generator.get_pipelines_graph()

        sorted_nodes = topological_sort(graph)

        self.__orchestration_notebook_generator.generate(list(sorted_nodes))
