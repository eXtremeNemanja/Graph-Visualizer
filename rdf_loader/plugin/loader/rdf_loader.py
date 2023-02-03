from rdflib import Graph
from plugin.core.services.loader import BaseLoader
from plugin.core.models import Vertex
from plugin.core.models import Graph as G


class RdfLoader(BaseLoader):
    def __init__(self) -> None:
        self.id_counter = 0
        self.graph = None

    def identifier(self):
        return "rdf-loader"

    def name(self):
        return "RDF Loader"

    def create_vertex(self, node, graph):
        for vertex in graph.vertices:
            if vertex.attributes["name"] == node:
                return vertex

        self.id_counter += 1
        v = Vertex(self.id_counter)
        v.attributes["name"] = node
        self.graph.insert_vertex(v)
        return v

    def populate_graph(self, nodes):
        (subject, predicate, object) = nodes
        first_vertex = self.create_vertex(subject, self.graph)
        second_vertex = self.create_vertex(object, self.graph)
        self.graph.insert_edge(first_vertex, second_vertex, True, predicate)

    def load_file(self, file):
        g = Graph()
        g.parse(file)
        return g

    def make_graph(self, data):
        self.graph = G()
        for row in data:
            self.populate_graph(row)
        return self.graph
