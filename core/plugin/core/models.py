from django.db import models


class Graph(object):

    __slots__ = '_name', '_vertices'

    def __init__(self, name):
        self._name = name
        self._vertices = []

    @property
    def vertices(self):
        return self._vertices

    @vertices.setter
    def vertices(self, vertices):
        self._vertices = vertices

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def edges(self):
        result = set()      
        for vertex in self._vertices():
            result.update(vertex.edges())    
        return result

    def degree(self, v):
        return v.degree()

    def _validate_vertex(self, v):
        if not isinstance(v, self.Vertex):
            raise TypeError('Object of Vertex class was excpected.')
        if v not in self._outgoing:
            raise ValueError("Vertex doesn't belong to this graph.")

    def vertex_count(self):
        return len(self._vertices)

    def edge_count(self):
        for edge in self.edges():
            if edge.is_directed():
                total_directed += 1
            else:
                total_undirected += 1    
        return total_directed + total_undirected//2

    def insert_vertex(self, v=None):
        self._vertices.append(v)

    def insert_edge(self, u, v, is_directed, relation, weight=None):
        e = Edge(u, v, relation, weight, is_directed)
        u.add_edge(e)
        if not is_directed:
            v.add_edge(e)


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

    def degree(self):
        return len(self._edges)

    def add_attribute(self, key, value):
        self._attributes[key] = value

    def add_edge(self, edge):
        self._edges.append(edge)

    def __hash__(self):
        return hash(self._id)

    def __eq__(self, other) -> bool:
        if self._id == other.id:
            return True
        if "id" in self._attributes and "id" in other.attributes:
            if self._attributes["id"] == other.attributes["id"]:
                return True
            return False
        
        if self._attributes != other.attributes:
            return False
        
        if len(self._edges) != len(other.edges):
            return False
        
        for edge in self._edges:
            for e in other.edges:
                if edge == e:
                    break
            else:
                return False
        
        return True
        


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

    def __eq__(self, other) -> bool:
        if self._weight != other.weight:
            return False
        elif self._relation_name != other.relation_name:
            return False
        elif self._is_directed != other.is_directed:
            return False
        elif self._destination != other.destination:
            return False

        #TODO: how to compare sources without recursion error?
        # elif self._source != other.source:
        #     return False
        
        return True
