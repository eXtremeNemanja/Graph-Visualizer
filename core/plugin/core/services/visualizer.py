from abc import abstractmethod
from service_base import ServiceBase

class BaseVisualizer(ServiceBase):
    @abstractmethod
    def visualize(self, graph):
        pass
