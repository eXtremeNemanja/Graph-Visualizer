
class Graph(object):

    __slots__ = '_name', '_vertices', 'visited', 'path', 'nodes_to_contour'

    def __init__(self):
        self._vertices = []
        self.visited = []
        self.path = []
        self.nodes_to_contour = []

    @property
    def vertices(self):
        return self._vertices

    @vertices.setter
    def vertices(self, vertices):
        self._vertices = vertices

    def edges(self):
        result = set()
        for vertex in self._vertices:
            result.update(vertex.edges)
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
        already_existing = self.contains_vertex(v)
        if already_existing:
            self._vertices[self._vertices.index(already_existing)] = v
        else:
            self._vertices.append(v)

    def insert_edge(self, u, v, is_directed, relation, weight=None):
        e = Edge(u, v, relation, weight, is_directed)
        u.add_edge(e)
        if not is_directed:
            v.add_edge(e)

    def contains_vertex(self, v):
        for vertex in self.vertices:
            if v == vertex:
                return vertex
        return None

    def find_subgraphs(self, vertices=[], graphs=[]):
        changes = True
        if not vertices:
            vertices = self.vertices

        connected = {}
        for vertex in vertices:
            if len(connected) == 0:
                connected[vertex] = True
            else:
                connected[vertex] = False

        if list(connected.values()) == [True * len(vertices)]:
            subgraph = Graph("x")
            subgraph.vertices = list(connected.keys())
            graphs.append(subgraph)
            return graphs

        while changes:
            changes = False
            for v in vertices:
                if connected[v]:
                    if self.check_as_true(v.edges, connected):
                        changes = True
                else:
                    if self.check_if_true(v, connected):
                        connected[v] = True
                        if self.check_as_true(v.edges, connected):
                            changes = True

        if list(connected.values()) == [True for i in range(len(connected.values()))]:
            subgraph = Graph("x")
            subgraph.vertices = list(connected.keys())
            graphs.append(subgraph)
            return graphs

        removed = self.remove_connected_vertices(vertices, connected)
        subgraph = Graph("x")
        subgraph.vertices = removed
        graphs.append(subgraph)
        return self.find_subgraphs(vertices, graphs)

    def check_if_true(self, vertex, connected):
        for edge in vertex.edges:
            if connected[edge.source]:
                return True
            elif connected[edge.destination]:
                return True

        return False

    def check_as_true(self, edges, connected):
        changes = False
        for edge in edges:
            if connected[edge.source] is False:
                changes = True
            elif connected[edge.destination] is False:
                changes = True
            connected[edge.source] = True
            connected[edge.destination] = True

        return changes

    def remove_connected_vertices(self, vertices, connected):
        removed = []
        for v in connected.keys():
            if connected[v]:
                vertices.remove(v)
                removed.append(v)

        return removed

    def is_graph_directed(self):
        if len(self.edges()) > 0:
            return list(self.edges())[0].is_directed

    def depth_first_search(self, current, parent):
        self.visited.append(current)
        for vertex in self.vertices:
            if current.is_related(vertex):
                if parent and vertex == parent:
                    continue
                if vertex in self.visited:
                    if vertex != self.visited[-1]:
                        return True
                elif self.depth_first_search(vertex, current):
                    return True
        return False

    def has_cycle_undirected(self):
        self.visited = []
        for vertex in self.vertices:
            if vertex in self.visited:
                if vertex != self.visited[-1]:
                    continue
            if self.depth_first_search(vertex, None):
                return True
        return False

    def has_cycle_directed(self, v):
        if v in self.path:
            if self.path[0] not in self.nodes_to_contour:
                self.nodes_to_contour.append(self.path[0])
            return
        if v in self.visited:
            return
        self.path.append(v)
        for edge in v.edges:
            self.has_cycle_directed(edge.destination)
        if v not in self.nodes_to_contour:
            self.visited.append(v)

    def find_conture_nodes(self):
        self.nodes_to_contour = []
        self.visited = []
        for vertex in self.vertices:
            if vertex not in self.nodes_to_contour:
                self.path = []
                self.has_cycle_directed(vertex)

        return self.nodes_to_contour

    # finds vertices that don't have incoming edges
    def find_not_destination_vertices(self):
        dict = {}
        for vertex in self.vertices:
            dict[vertex] = False

        for edge in self.edges():
            dict[edge.destination] = True

        roots = []
        for vertex in dict.keys():
            if dict[vertex] is False:
                roots.append(vertex)

        return roots


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

    def add_edge(self, e):
        already_existing = self.contains_edge(e)
        if already_existing:
            self._edges[self._edges.index(already_existing)] = e
        else:
            self._edges.append(e)

    def contains_edge(self, e):
        for vertex in self._edges:
            if e == vertex:
                return vertex
        return None

    def relations(self):
        relations = []
        for edge in self._edges:
            if edge.relation_name in relations:
                continue
            relations.append(edge.relation_name)
        return relations

    def related_vertices(self, relation):
        vertices = []
        for edge in self._edges:
            if edge.relation_name == relation:
                if edge.source == self:
                    vertices.append(edge.destination)
        return vertices

    def is_related(self, vertex):
        for edge in self.edges:
            if edge.source == self:
                if edge.destination == vertex:
                    return True
            elif edge.destination == self:
                if edge.source == vertex:
                    return True
        return False

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

        #TODO: how to compare sources without recursion error?
        # for edge in self._edges:
        #     for e in other.edges:
        #         if edge == e:
        #             break
        #     else:
        #         return False
        
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


class NodeIdGenerator:

    def __init__(self):
        self.__current_id = 0

    def next(self):
        self.__current_id += 1
        return self.__current_id - 1

    def reset(self):
        self.__current_id = 0


nodeId = NodeIdGenerator()


class TreeNode(object):
    __slots__ = '_opened', '_object', '_object_type', '_children', '_id', '_parent'

    def __init__(self, object, parent, type):
        self._opened = False
        self._object = object
        self._object_type = type
        self._id = nodeId.next()
        self._children = []
        self._parent = parent

    @property
    def id(self):
        return self._id

    @property
    def opened(self):
        return self._opened

    @opened.setter
    def opened(self, value):
        self._opened=value

    def open(self):
        self._opened = True
        if len(self._children) <= 0:
            if self._object_type == "vertex":
                self.add_children(self._object.relations())
            else:
                self.add_children(self._parent.object.related_vertices(self._object))

    def close(self):
        self._opened = False
        # for child in self._children:
        #     child.opened = False

    @property
    def object(self):
        return self._object

    @property
    def object_type(self):
        return self._object_type

    @property
    def children(self):
        return self._children

    @property
    def parent(self):
        return self._parent

    def find_node(self, id):
        if id == self._id:
            return self
        else:
            for child in self._children:
                found_node = child.find_node(id)
                if found_node:
                    return found_node

    def add_children(self, children_objects):
        for child in children_objects:
            if self._object_type == "vertex":
                child_type = "edge"
                child_node = TreeNode(child, self, child_type)
                # child_node.opened = True
                self._children.append(child_node)
            else:
                child_type = "vertex"
                # for related in self.parent.object.related_vertices(self.object):
                child_node = TreeNode(child, self, child_type)
                self._children.append(child_node)



class Forest(object):
    __slots__ = '_roots', '_last_opened'

    def __init__(self, roots=None):
        nodeId.reset()
        self._roots = roots
        if self._roots is None:
            self._roots = []
        self._last_opened = 0

    @property
    def roots(self):
        return self._roots

    @roots.setter
    def roots(self, roots):
        self._roots = roots

    @property
    def last_opened(self):
        return self._last_opened

    @last_opened.setter
    def last_opened(self, last_opened):
        self._last_opened = last_opened

    def find_tree_node(self, id):
        for root_node in self._roots:
            found_node = root_node.find_node(id)
            if found_node:
                return found_node





