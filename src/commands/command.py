from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def apply(self):
        pass