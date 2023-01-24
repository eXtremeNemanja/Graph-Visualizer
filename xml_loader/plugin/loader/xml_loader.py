import os

from core.plugin.core.services.loader import BaseLoader
import xml.etree.ElementTree as ET

from tim05.core.plugin.core.models import Vertex, Edge, Graph

class XmlLoader(BaseLoader):
    __slots__ = 'id_counter'

    def __init__(self) -> None:
        self.id_counter = 0

    def identifier(self):
        return "XmlLoader"

    def name(self):
        return "Loading data from xml document"

    def get_file_name(self, file_name):
        return os.path.join(os.path.dirname(__file__), "..", "..", "..", "datasets", "xml", file_name)

    def load_file(self, file_name):
        file_name = self.get_file_name(file_name)
        tree = ET.parse(file_name)
        root = tree.getroot()
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
            v.add_attribute("text", node.text)
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

    def make_graph(self, tree, graph_name):
        g = Graph(graph_name)
        self.create_vertex(g, tree)
        return g