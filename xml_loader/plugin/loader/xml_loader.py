import os

from plugin.core.services.loader import BaseLoader
import xml.etree.ElementTree as ET

from plugin.core.models import Vertex, Edge, Graph

class XmlLoader(BaseLoader):
    __slots__ = 'id_counter', 'unique_key'

    def __init__(self) -> None:
        self.id_counter = 0
        self.unique_key = "id"

    def identifier(self):
        return "xml-loader"

    def name(self):
        return "XML Loader"

    # def get_file_name(self, file_name):
    #     return os.path.join(os.path.dirname(__file__), "..", "..", "..", "datasets", "xml", file_name)

    def load_file(self, file, unique_key="id"):
        self.unique_key = unique_key
        # file_name = self.get_file_name(file_name)
        # with open(file_name, 'r') as file:
        tree_string = file.read()
        root = ET.fromstring(tree_string)
        return root

    def create_vertex(self, graph, node):
        # print("-------------")
        self.id_counter += 1
        v = Vertex(self.id_counter)
        for key in node.attrib:
            v.add_attribute(key, node.attrib.get(key))
        node.text = node.text.strip()
        if node.text:
            node.text = " ".join(node.text.split())
            # print(node.text)
            v.add_attribute(node.tag, node.text)
        # for att in v.attributes:
        #     print(att)
        # id="bk101"
        for child in node:
            c = self.create_vertex(graph, child)
            e = Edge(v, c, child.tag, 0, True)
            v.add_edge(e)
        for vertex in graph.vertices:
            if v == vertex:
                # print("Isti")
                return vertex
        graph.insert_vertex(v)
        return v

    def make_graph(self, tree):
        g = Graph()
        self.create_vertex(g, tree)
        return g
