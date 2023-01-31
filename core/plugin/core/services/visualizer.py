from abc import abstractmethod

from plugin.core.services.service_base import ServiceBase

class BaseVisualizer(ServiceBase):
    @abstractmethod
    def visualize(self, graph):
        pass
