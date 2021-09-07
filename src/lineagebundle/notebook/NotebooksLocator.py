from logging import Logger
from pathlib import Path


class NotebooksLocator:
    def __init__(
        self,
        project_base_dir: str,
        paths_patterns: list,
        logger: Logger,
    ):
        self.__project_base_dir = Path(project_base_dir)
        self.__paths_patterns = paths_patterns
        self.__logger = logger

    def locate(self):
        def is_notebook_with_decorators(path: Path):
            with path.open("r", encoding="utf-8") as f:
                content = f.read()

                return "@transformation(" in content or "@notebook_function(" in content

        def create_notebook(path: Path):
            self.__logger.debug(f"Reading {path}")

            return path.relative_to(self.__project_base_dir.parent)

        base_dir = self.__project_base_dir
        files_grabbed = []

        for path_pattern in self.__paths_patterns:
            files_grabbed.extend(base_dir.glob(path_pattern))

        return [
            create_notebook(path)
            for path in files_grabbed
            if not path.match(".ipynb_checkpoints/*.py") and is_notebook_with_decorators(path)
        ]
