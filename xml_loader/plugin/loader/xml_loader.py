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

    def make_graph(self, tree):
        return super().make_graph(tree)