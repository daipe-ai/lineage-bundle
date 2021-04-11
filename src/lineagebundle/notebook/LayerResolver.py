import re


class LayerResolver:
    def __init__(self, pattern: str):
        self.__pattern = pattern

    def resolve(self, notebook_path: str):
        regexp = re.compile(self.__pattern.replace("{layer}", "([^/]+)"))

        match = re.match(regexp, notebook_path)

        if not match:
            raise Exception("Layer pattern does not match notebook path")

        if len(match.groups()) < 1:
            raise Exception("Layer pattern does not contain layer placeholder")

        return match.group(1)
