from plugin.core.services.visualizer import BaseVisualizer
from plugin.core.models import Vertex, Edge, Graph

class ComplexVisualizer(BaseVisualizer):
    def identifier(self):
        return "ComplexVisualizer"

    def name(self):
        return "Show graph with complex view"

    def visualize(self, graph):
        return super().visualize(graph)