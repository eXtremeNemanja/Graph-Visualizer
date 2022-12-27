from django.db import models

class Vertex:
    __slots__ = '_attributes', '_id', '_edges'

    def __init__(self, id):
        self._attributes = {}
        self._id = id
        self._edges = []

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        self._attributes = attributes

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def edges(self):
        return self._edges

    @edges.setter
    def edges(self, edges):
        self._edges = edges

    def add_attribute(self, key, value):
        self._attributes[key] = value

    def add_edge(self, edge):
        self._edges.append(edge)

    def __hash__(self):
        return hash(self._id)


class Edge:
    __slots__ = '_source', '_destination', '_relation_name', '_weight', '_is_directed'

    def __init__(self, source, destination, relation_name, weight, is_directed):
        self._source = source
        self._destination = destination
        self._relation_name = relation_name
        self._weight = weight
        self._is_directed = is_directed

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, source):
        self._source = source

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, destination):
        self._destination = destination

    @property
    def relation_name(self):
        return self._relation_name

    @relation_name.setter
    def relation_name(self, name):
        self._relation_name = name

    @property
    def is_directed(self):
        return self._is_directed

    @is_directed.setter
    def is_directed(self, is_directed):
        self._is_directed = is_directed

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, weight):
        self._weight = weight

    def endpoints(self):
        return self._source, self._destination

    def get_opposite(self, v):
        if not isinstance(v, Vertex):
            raise TypeError('v has to be an instance of vertex class')
        if self._destination == v:
            return self._source
        elif self._source == v:
            return self._destination
        raise ValueError('v is not vertex of this edge')

    def __hash__(self):  
        return hash((self._source, self._destination))

    def __str__(self):
        return '({0},{1},{2},{3},{4})'.format(self._source, self._destination, self._relation_name,
                                                  self._weight, self._is_directed)

