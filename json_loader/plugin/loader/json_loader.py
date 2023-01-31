import datetime
from abc import ABC

from plugin.core.models import Graph, Vertex, Edge
from plugin.core.services.loader import BaseLoader
import json


class JsonLoader(BaseLoader, ABC):

    __slots__ = '_id_counter', '_dataset_name'

    def __init__(self):
        self._id_counter = 0
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

