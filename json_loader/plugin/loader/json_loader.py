import numbers

from plugin.core.models import Graph, Vertex, Edge
from plugin.core.services.loader import BaseLoader
import json


def isPrimitive(value):
    return isinstance(value, (str, numbers.Number))


class JsonLoader(BaseLoader):

    __slots__ = '_id_counter', '_graph'

    def __init__(self):
        self._id_counter = 0
        self._unique_key = "id"
        self._graph = None

    def identifier(self):
        return "json-loader"

    def name(self):
        return "JSON Loader"

    def load_file(self, file, unique_key="id"):
        self._unique_key = unique_key
        json_object = json.load(file)
        return json_object

    def make_graph(self, tree):
        self._graph = Graph()
        self.create_vertex(tree)
        return self._graph

    def create_vertex(self, data, parent_vertex=None, relationship=None):
        # TODO add weight on edges
        # TODO non directional edge logic
        current_vertex = Vertex(None)
        for nested_item in data:
            if isinstance(nested_item, dict):                                      # nested_item -> object, data -> list of objects
                nested_vertex = self.create_vertex(nested_item, parent_vertex, relationship)
                nested_vertex.id = self.set_vertex_id(nested_item)
                self.update_graph(nested_vertex, parent_vertex, relationship)
            else:                                                                  # nested_item -> primitive, data -> object
                if not isinstance(data, list) and isPrimitive(data[nested_item]):  # nested_item -> attribute name
                    if nested_item == self._unique_key:
                        current_vertex.id = data[nested_item]
                        current_vertex.add_attribute("id", data[nested_item])
                    current_vertex.add_attribute(nested_item, data[nested_item])
                elif isinstance(data, list):                                       # data -> list of primitive items
                    nested_vertex = Vertex(nested_item)
                    nested_vertex.add_attribute("id", nested_item)
                    nested_vertex.add_attribute("value", nested_item)
                    self.update_graph(nested_vertex, parent_vertex, relationship)
                else:                                                              # nested_item -> object attribute
                    current_vertex = self.create_vertex(data[nested_item], current_vertex, nested_item)
        if not current_vertex.id:
            return parent_vertex
        self.alter_existing_vertex(current_vertex)
        return current_vertex

    def add_new_edge(self, child_vertex, parent_vertex, relationship):
        e = Edge(parent_vertex, child_vertex, relationship, 0, True)
        parent_vertex.add_edge(e)

    def update_graph(self, nested_vertex, parent_vertex, relationship):
        self.alter_existing_vertex(nested_vertex)
        self.add_new_edge(nested_vertex, parent_vertex, relationship)

    def alter_existing_edges(self, edges, vertex):
        for edge in edges:
            if edge.source == vertex:
                edge.source = vertex
                vertex.add_edge(edge)
            elif edge.destination == vertex:
                edge.destination = vertex
                edge.source.add_edge(edge)

    def alter_existing_vertex(self, vertex):
        already_in_graph = self._graph.contains_vertex(vertex)
        if already_in_graph:
            vertex.attributes.update(already_in_graph.attributes)
            self.alter_existing_edges(self._graph.edges(), vertex)
        self._graph.insert_vertex(vertex)

    def set_vertex_id(self, vertex_data=None):
        if vertex_data and self._unique_key in vertex_data.keys():
            vertex_id = vertex_data[self._unique_key]
        else:
            vertex_id = self.next_id()
        return vertex_id

    def next_id(self):
        current_id = self._id_counter
        self._id_counter += 1
        return current_id


if __name__ == '__main__':

    pl = JsonLoader()
    with open("../../../datasets/json/people.json") as file:
        data=pl.load_file(file)
    g = pl.make_graph(data)
    print("a")
