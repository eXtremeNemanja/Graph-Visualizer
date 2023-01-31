from plugin.core.services.visualizer import BaseVisualizer

class SimpleVisualizer(BaseVisualizer):

    def identifier(self):
        return "SimpleVisualizer"

    def name(self):
        return "Show graph with simple view"

    def visualize(self, graph):
        return super().visualize(graph)
