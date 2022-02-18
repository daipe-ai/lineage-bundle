import networkx as nx
from consolebundle.ConsoleCommand import ConsoleCommand
from lineagebundle.lineage.LineageGenerator import LineageGenerator


class LineageImagePublisherCommand(ConsoleCommand):
    def __init__(
        self,
        lineage_generator: LineageGenerator,
    ):
        self.__lineage_generator = lineage_generator

    def get_command(self) -> str:
        return "lineage:publish:image"

    def get_description(self):
        return "Creates database as an image"

    def run(self, _):
        try:
            import matplotlib.pyplot as plt  # pylint: disable = import-outside-toplevel # pyre-ignore[21]:
        except ImportError:
            raise Exception("This command requires matplotlib, which is not installed.")  # pylint: disable = raise-missing-from

        graph = self.__lineage_generator.pipelines_graph
        nx.draw_planar(graph, with_labels=True)
        plt.savefig("lineage/lineage.png")
