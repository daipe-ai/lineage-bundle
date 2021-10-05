import os
from box import Box
from lineagebundle.notebook.Notebook import Notebook
from lineagebundle.publish.HTMLCreator import HTMLCreator
from logging import Logger
from pathlib import Path
from typing import List


class OrchestrationNotebookGenerator:
    def __init__(
        self,
        logger: Logger,
        root_module: Box,
        orchestration_notebook_relpath: str,
        html_creator: HTMLCreator,
    ):
        self.__logger = logger
        self.__root_module_name = root_module.name
        self.__project_base_dir = Path(root_module.path)
        self.__orchestration_notebook_relpath = Path(orchestration_notebook_relpath)
        self.__html_creator = html_creator
        self.__orchestration_notebook_path = Path(self.__project_base_dir).joinpath(self.__orchestration_notebook_relpath)

    def generate(self, sorted_nodes: List[Notebook]):
        rel_height = len(self.__orchestration_notebook_relpath.parents) - 1
        install_master_package_path = f"./{'../' * rel_height}app/install_master_package"

        def prepare_path(node):
            notebook_path = Path(node.path)
            notebook_path_no_suffix = notebook_path.parent.joinpath(notebook_path.stem)
            return notebook_path_no_suffix.relative_to(Path(self.__root_module_name)).as_posix()

        cell_code = "\n".join(f"{' ' * 4}dbutils.notebook.run(\"./{'../' * rel_height}{prepare_path(node)}\", 0)" for node in sorted_nodes)

        template_path = os.path.join(os.path.dirname(__file__), "templates/template.txt")

        with open(template_path) as file:
            notebook_code = file.read()

        notebook_code = (
            notebook_code.replace("INSTALL_MASTER_PACKAGE_PATH", install_master_package_path)
            .replace("CELL_CODE", cell_code)
            .replace("LINEAGE_HTML", self.__html_creator.create_pipelines_html_code(sorted_nodes, on_tap_enabled=False))
        )

        self.__orchestration_notebook_path.parent.mkdir(parents=True, exist_ok=True)

        with self.__orchestration_notebook_path.open("w") as orchestration_notebook:
            self.__logger.info(f"Writing {orchestration_notebook.name}")
            orchestration_notebook.write(notebook_code)
