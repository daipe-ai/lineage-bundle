from abc import ABC, abstractmethod


class ParsedDecorator(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass
