import os

from core.plugin.core.services.loader import BaseLoader
import xml.etree.ElementTree as ET

from tim05.core.plugin.core.models import Vertex, Edge, Graph

class XmlLoader(BaseLoader):
    def identifier(self):
        return "XmlLoader"

    def name(self):
        return "Loading data from xml document"

    def load_file(self, file_name):
        tree = ET.parse(file_name)
        root = tree.getroot()
        return root

    def create_vertex(graph, node, id_counter):
        id_counter
        v = Vertex(id_counter)
        for key in node.attrib:
            v.add_attribute(key, node.attrib.get(key))
        if node.text != "":
            v.add_attribute("text", node.text)
        v.add_attribute()
        graph.insert_vertex(v)
        for child in node:
            c = create_vertex(graph, child, id_counter)
            e = Edge(v, c, c.tag, 0, True)
            v.add_edge(e)
        return v

    def make_graph(self, tree, graph_name):
        g = Graph(graph_name)
        create_vertex(g, tree, 0)