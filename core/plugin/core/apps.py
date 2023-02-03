import pkg_resources
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    loaders = []
    visualizers = []
    name = 'plugin.core'
    base_graph = None
    current_graph = None

    def ready(self):
        # Prilikom startovanja aplikacije, ucitavamo plugine na
        # vec poznati nacin.
        self.loaders = load_plugins("loader")
        self.visualizers = load_plugins("visualizer")
        
    def find_root_vertices_for_treeview(self):
        subgraphs = self.current_graph.find_subgraphs()
        return find_root_vertices(subgraphs)


def load_plugins(oznaka):
    plugins = []
    for ep in pkg_resources.iter_entry_points(group=oznaka):
        p = ep.load()
        print("{} {}".format(ep.name, p))
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

