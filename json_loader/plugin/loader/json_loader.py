import datetime
import numbers

from plugin.core.models import Graph, Vertex, Edge
from plugin.core.services.loader import BaseLoader
import json

def isPrimitive(value):
    return isinstance(value, (str, numbers.Number))


class JsonLoader(BaseLoader):

    __slots__ = '_id_collection', '_dataset_name'

    def __init__(self):
        self._id_collection = {}
        self._dataset_name = ""

    def identifier(self):
        return "JsonLoader"

    def name(self):
        return "Loading data from json document"

    def load_file(self, file_name):
        self._dataset_name = file_name
        with open(file_name, 'r') as file:
            jsonObject = json.load(file)
        return jsonObject

    def make_graph(self, tree):
        g = Graph(self._dataset_name)
        return g


    def create_vertex(self, graph, data):
        v = Vertex(None)
        for nested_object in data:
            # current item is object in data
            if isinstance(nested_object, dict):
                v = self.set_vertex_id(v, nested_object)
                self.create_vertex(graph, nested_object)
            # current item is list in data
            elif isinstance(nested_object, list):
                self.create_vertex(graph, nested_object)
            # current item has primitive type
            else:
                # current item is primitive attribute of data object
                if not isinstance(data, list) and isPrimitive(data[nested_object]):
                    v.add_attribute(nested_object, data)
                # data is list of primitive types
                elif isinstance(data, list):
                    nested_v = Vertex(None)
                    nested_v = self.set_vertex_id(nested_v)
                # current item is object attribute of data object
                else:
                    self.create_vertex(graph, data[nested_object])


    def set_vertex_id(self, vertex, object=None):
        if object and "id" in object.keys():
            id = object["id"]
        else:
            id = self.next_id()
        vertex.id = id
        if id in self._id_collection.keys():
            vertex = self._id_collection[id]
        self._id_collection[vertex.id] = vertex
        return vertex

    def next_id(self):
        return max([x for x in self._id_collection.keys() if isinstance(x, numbers.Number)]) + 1


if __name__ == '__main__':

    jl = JsonLoader()
    d = jl.load_file("../../../datasets/json/got-characters.json")
    g = jl.make_graph(d)
    jl.create_vertex(g, d)
