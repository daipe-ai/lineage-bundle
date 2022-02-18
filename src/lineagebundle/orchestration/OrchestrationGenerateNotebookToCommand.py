from argparse import ArgumentParser, Namespace
from consolebundle.ConsoleCommand import ConsoleCommand
from lineagebundle.lineage.LineageGenerator import LineageGenerator
from lineagebundle.orchestration.OrchestrationNotebookGenerator import OrchestrationNotebookGenerator
from logging import Logger
from networkx import topological_sort, has_path


class OrchestrationGenerateNotebookToCommand(ConsoleCommand):
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
        return "orchestration:generate:notebook:to"

    def get_description(self):
        return "Generates an orchestration notebook to run a specified notebook with all its prerequisities"

    def configure(self, argument_parser: ArgumentParser):
        argument_parser.add_argument(dest="label", help="Notebook label")

    def run(self, input_args: Namespace):
        self.__logger.info("Generating orchestration notebook...")
        graph = self.__lineage_generator.pipelines_graph

        filtered_nodes = filter(lambda notebook: notebook.label == input_args.label, graph.nodes)
        try:
            target_node = next(filtered_nodes)
        except StopIteration:
            raise Exception(f"No such notebook: {input_args.label}")  # pylint: disable = raise-missing-from

        sorted_notebooks = topological_sort(graph)

        nodes = []
        for notebook in sorted_notebooks:
            if has_path(graph, source=notebook, target=target_node):
                nodes.append(notebook)

            if notebook.label == input_args.label:
                break

        self.__orchestration_notebook_generator.generate(nodes)
