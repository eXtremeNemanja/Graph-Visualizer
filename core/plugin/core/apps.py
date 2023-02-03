import pkg_resources
from django.apps import AppConfig

import os

from plugin.core.models import Forest, TreeNode


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    loaders = []
    visualizers = []
    name = 'plugin.core'
    base_graph = None
    current_graph = None
    tree = None
    current_visualizer = None

    def ready(self):
        # Prilikom startovanja aplikacije, ucitavamo plugine na
        # vec poznati nacin.
        print("Getting ready...")
        self.loaders = load_plugins("loader")
        self.visualizers = load_plugins("visualizer")
        
    def find_root_vertices_for_treeview(self):
        subgraphs = self.current_graph.find_subgraphs()
        return find_root_vertices(subgraphs)

    def get_loader(self, id):
        print(id)
        for l in self.loaders:
            print(l.identifier())
            if l.identifier() == id:
                return l
        return None

    def get_visualizer(self, id):
        print(id)
        for v in self.visualizers:
            print(v.identifier())
            if v.identifier() == id:
                return v
        return None

    def load_tree(self):
        self.tree = Forest(None)
        for vertex in find_root_vertices(self.current_graph.find_subgraphs()):
            self.tree.roots.append(TreeNode(vertex, None, "vertex"))

def load_plugins(entry_point):
    plugins = []
    print(entry_point)
    for ep in pkg_resources.iter_entry_points(group=entry_point):
        print(ep)
        p = ep.load()
        print("Loading plugin ...{} {}".format(ep.name, p))
        plugin = p()
        plugins.append(plugin)
    return plugins


def find_root_vertices(subgraphs):
    roots = []
    for graph in subgraphs:
        if graph.is_graph_directed():
            contour_nodes = graph.find_conture_nodes()
            hanging_nodes = graph.find_not_destination_vertices()
            roots += merge_lists_distinct(contour_nodes, hanging_nodes)

        else:
            if graph.has_cycle_undirected():
                if len(graph.vertices) > 0:
                    roots.append(graph.vertices[0])
            else:
                for v in graph.vertices:
                    if v.degree() <= 1:
                        roots.append(v)

    return roots


def merge_lists_distinct(first_list, second_list):
    for i in first_list:
        if i not in second_list:
            second_list.append(i)

    return second_list

