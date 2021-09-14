from abc import ABC, abstractmethod
from sqlalchemybundle.entity.Base import Base
from typing import List


class PublisherInterface(ABC):
    @abstractmethod
    def publish(self, entities: List[Base]):
        pass
