import pkg_resources
from django.apps import AppConfig

import os

from core.plugin.core.models import Forest, TreeNode


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    loaders = []
    visualizers = []
    name = 'plugin.core'
    base_graph = None
    current_graph = None
    tree = None

    def ready(self):
        # Prilikom startovanja aplikacije, ucitavamo plugine na
        # vec poznati nacin.
        print("Getting ready...")
        self.loaders = load_plugins("loader")
        self.visualizers = load_plugins("visualizer")

    def get_loader(self, id):
        print(id)
        for l in self.loaders:
            print(l.identifier())
            if l.identifier() == id:
                return l
        return None

    def load_tree(self):
        self.tree = Forest()
        for vertex in self.base_graph.vertices:
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
    
