from abc import abstractmethod
from service_base import ServiceBase

class BaseLoader(ServiceBase):
    @abstractmethod
    def load_file(self):
        pass

    @abstractmethod
    def make_graph(self):
        pass