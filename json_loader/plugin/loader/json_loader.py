import datetime

from plugin.core.models import Graph, Vertex, Edge
import json


# class JsonLoader(DataService):
class JsonLoader():
    def __init__(self):
        self.__path = ""
        self.__id_gen = self.__id_generator()
        self.__name_gen = self.__name_generator()
        self.__list_gen = self.__list_generator()
        self.__graph = None
        self.__reference_ids = {}
        self.__references = {}

    def load(self):
        # try:
        with open(self.__path, "r") as read_file:
            file = json.load(read_file)
            self.__graph = Graph()

            if isinstance(file, list):
                self.make_Vertex_from_list(file)
            else:
                self.__parse_Vertex(file, "root_Vertex")


        # except:
        #     raise Exception("Parisranje nije uspelo")
        self.__references = {}
        self.__reference_ids = {}

    def make_Vertex_from_list(self, Vertex_list, parent_Vertex=None):
        i = 0
        Vertex = Vertex(next(self.__id_gen), name=next(self.__list_gen))
        self.__graph.add_Vertex(Vertex)
        if parent_Vertex is not None:
            self.__graph.add_Edge(parent_Vertex, Vertex)


        for el in Vertex_list:
            if isinstance(el, dict):
                self.__parse_Vertex(el, next(self.__name_gen), Vertex)
            elif isinstance(el, list):
                self.make_Vertex_from_list(el, Vertex)
            elif isinstance(el, str):
                try:
                    attr_float = float(el)
                    el = attr_float
                except ValueError:
                    date = self.try_parse_date(el,
                                               ["%d/%m/%Y", "%Y/%m/%d", "%d/%m/%Y %H:%M:%S", "%Y/%m/%d %H:%M:%S"])
                    if date is not None:
                        el = date

                Vertex.add_attribute("list_elem" + str(i), el)
                i += 1

            else:
                Vertex.add_attribute("list_elem" + str(i), el)
                i += 1

    def get_graph(self) -> Graph:
        return self.__graph

    def identifier(self):
        return "json-loades"

    def name(self):
        return "JSON loader"

    def set_path(self, path: str):
        self.__path = path

    def __id_generator(self):
        self.num = 0
        while True:
            yield "ID" + str(self.num)
            self.num += 1

    def __name_generator(self):
        self.gen = 0
        while True:
            yield "object" + str(self.gen)
            self.gen += 1

    def __list_generator(self):
        self.gen = 0
        while True:
            yield "list_obj_" + str(self.gen)
            self.gen += 1

    def try_parse_date(self, str_date, formats):
        for format in formats:
            try:
                str_date = datetime.datetime.strptime(str_date, format)
                return str_date
            except ValueError:
                pass
        return None

    def __parse_Vertex(self, Vertex, name, parent_Vertex=None):
        new_Vertex = Vertex(next(self.__id_gen), name=name)
        self.__graph.add_Vertex(new_Vertex)
        for attr, val in Vertex.items():
            if attr == "id":
                self.__reference_ids[val] = new_Vertex
                continue
            if attr == "references":
                self.__references[new_Vertex] = val
                continue
            if parent_Vertex is not None:
                self.__graph.add_Edge(parent_Vertex, new_Vertex)
            if isinstance(val, list):
                self.make_Vertex_from_list(val, new_Vertex)
                continue
            if isinstance(val, str):
                try:
                    attr_float = float(val)
                    val = attr_float
                except ValueError:
                    date = self.try_parse_date(val,
                                               ["%d/%m/%Y", "%Y/%m/%d", "%d/%m/%Y %H:%M:%S", "%Y/%m/%d %H:%M:%S"])
                    if date is not None:
                        val = date

            if isinstance(val, dict):
                self.__parse_Vertex(val, attr, new_Vertex)
            else:
                new_Vertex.add_attribute(attr, val)
        self.set_reference_Edges()

    def __get_Vertexs_from_list(self, parent_Vertex, Vertexs):
        for Vertex in Vertexs:
            self.__parse_Vertex(Vertex, parent_Vertex)

    def set_reference_Edges(self):
        try:
            for Vertex, refs in self.__references.items():
                for key, val in self.__reference_ids.items():
                    if key in refs:
                        self.__graph.add_Edge(Vertex, val)
        except KeyError:
            pass

