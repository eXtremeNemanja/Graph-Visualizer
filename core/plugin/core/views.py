import os
import time
from datetime import datetime, date
from django.shortcuts import render, redirect
from django.urls import reverse
from django.apps.registry import apps
from .models import Edge, Graph, Vertex
from django.http import HttpResponse
from django.template.loader import render_to_string


# Create your views here.
from django.http import HttpResponse


def index(request, file_missing=False):
    print("Log",  "Logging")
    graph = apps.get_app_config('core').current_graph
    tree = apps.get_app_config('core').tree
    visualizers = []
    for v in apps.get_app_config('core').visualizers:
        visualizers.append({"name": v.name(), "identifier": v.identifier()})
    loaders = []
    for l in apps.get_app_config('core').loaders:
        loaders.append({"name": l.name(), "identifier": l.identifier()})
    
    return render(request, "index.html", {'graph': graph, 'tree': tree, 'visualizers': visualizers, 'loaders': loaders, 'file_missing': file_missing})


def reset(request):
    apps.get_app_config('core').current_graph = apps.get_app_config(
        'core').base_graph
    apps.get_app_config('core').load_tree()
    current_visualizer = apps.get_app_config('core').current_visualizer
    if (current_visualizer == "SimpleVisualizer"):
        return simple_visualization(request)
    elif (current_visualizer == "ComplexVisualizer"):
        return complex_visualization(request)
    else:
        if (apps.get_app_config('core').base_graph is None):
            return render(request, "index.html")
        else:
            return render(request, "index.html")


def new_data(request):
    apps.get_app_config('core').base_graph = None
    apps.get_app_config('core').current_graph = None
    apps.get_app_config('core').current_visualizer = None
    return redirect('index')


def load(request):
    plugini = apps.get_app_config('core').loaders
    chosen_file = None
    loader = None
    file_missing = False
    extension_missmatch = False
    if request.method == 'POST':
        loader = request.POST.get('loader', 'nema')
        chosen_file = request.FILES.get('file', None)
    unique_key = request.POST.get("key")
    # loader = apps.get_app_config('core').get_loader(request.POST.get('loader'))
    if not chosen_file:
        file_missing = True
    else:
        # file = request.FILES['file']
        # print(chosen_file)
        for p in plugini:
            # print(p.identifier())
            # print(loader)
            if p.identifier() == loader:
                if check_extension(loader, chosen_file):
                    root = p.load_file(chosen_file)
                    print(root)
                    apps.get_app_config('core').base_graph = p.make_graph(root)
                    print(apps.get_app_config('core').base_graph)
                    apps.get_app_config('core').current_graph = apps.get_app_config(
                        'core').base_graph
                    apps.get_app_config('core').load_tree()
                    path = os.path.abspath(os.path.dirname(__file__)) + \
                        "\\templates\\mainView.html"
                    with open(path, 'w+') as file:
                        file.write("")
                    time.sleep(2)
                else:
                    extension_missmatch = True



    visualizers = apps.get_app_config('core').visualizers
    loaders = apps.get_app_config('core').loaders
    visualizers = []
    for v in apps.get_app_config('core').visualizers:
        visualizers.append({"name": v.name(), "identifier": v.identifier()})
    loaders = []
    for l in apps.get_app_config('core').loaders:
        loaders.append({"name": l.name(), "identifier": l.identifier()})
    graph = apps.get_app_config('core').current_graph
    tree = apps.get_app_config('core').tree
    return render(request, "index.html", {'graph': graph, 'tree': tree, 'visualizers': visualizers, 'loaders': loaders, "file_missing": file_missing, "extension_missmatch": extension_missmatch})

    # return redirect("index")

def check_extension(loader, file):
    print(loader)
    print(file)
    match loader:
        case "XmlLoader":
            return file.name.endswith('.xml')
        case "RDFLoader":
            return file.name.endswith('.nt')
        case "JsonLoader":
            return file.name.endswith('.json')        
    return False


def visualize(request, type):
    visualizer = apps.get_app_config('core').get_visualizer(type)
    path = os.path.abspath(os.path.dirname(__file__)) + \
        "\\templates\\mainView.html"
    with open(path, 'w+') as file:
        file.write(visualizer.visualize(
            apps.get_app_config('core').base_graph, request))

    graph = apps.get_app_config('core').base_graph
    tree = apps.get_app_config('core').tree
    visualizers = []
    for v in apps.get_app_config('core').visualizers:
        visualizers.append({"name": v.name(), "identifier": v.identifier()})
    loaders = []
    for l in apps.get_app_config('core').loaders:
        loaders.append({"name": l.name(), "identifier": l.identifier()})
    return render(request, "index.html", {'graph': graph, 'tree': tree, 'visualizers': visualizers, 'loaders': loaders})

    return redirect('index')


def search(request, *args, **kwargs):
    # print(args, kwargs)
    query = request.GET.get("query", 'nema')
    if not apps.get_app_config('core').current_visualizer:
        if apps.get_app_config('core').base_graph is None:
            return render(request, 'index.html', {'search_error': True, 'graph': apps.get_app_config('core').base_graph})
        else:
            return render(request, 'index.html', {'search_error': True, 'graph': apps.get_app_config('core').base_graph})
    old_graph = apps.get_app_config('core').current_graph
    graph = Graph()
    for vertex in old_graph.vertices:
        search_vertex(graph, vertex, query)

    apps.get_app_config('core').current_graph = create_graph(old_graph, graph)
    apps.get_app_config('core').load_tree()

    current_visualizer = apps.get_app_config('core').current_visualizer
    if (current_visualizer == "SimpleVisualizer"):
        return simple_visualization(request)
    elif (current_visualizer == "ComplexVisualizer"):
        return complex_visualization(request)


def filter(request):
    query = request.GET.get("query", "")
    attribute, operator, value = parse_query(query)
    print(attribute, operator, type(value))

    old_graph = apps.get_app_config('core').current_graph
    graph = Graph()
    for vertex in old_graph.vertices:
        filter_vertex(graph, vertex, attribute, operator, value)

    apps.get_app_config('core').current_graph = create_graph(old_graph, graph)
    apps.get_app_config('core').load_tree()
    current_visualizer = apps.get_app_config('core').current_visualizer
    if (current_visualizer == "SimpleVisualizer"):
        return simple_visualization(request)
    elif (current_visualizer == "ComplexVisualizer"):
        return complex_visualization(request)
    else:
        return redirect('index')


def add_vertex(graph, vertex):
    new_vertex = Vertex(vertex.id)

    new_vertex_found = find_vertex_in_graph(graph, new_vertex)
    if not new_vertex_found:
        new_vertex.attributes.update(vertex.attributes)
    else:
        new_vertex = new_vertex_found

    for e in vertex.edges:
        destination = Vertex(e.destination.id)

        destination_found = find_vertex_in_graph(graph, destination)
        if not destination_found:
            destination.attributes.update(e.destination.attributes)
            graph.insert_vertex(destination)
        else:
            destination = destination_found

        new_vertex.add_edge(Edge(new_vertex, destination,
                            e.relation_name, e.weight, e.is_directed))

    # add if it isn't already added
    if not new_vertex_found:
        graph.insert_vertex(new_vertex)


def filter_vertex(graph, vertex, attribute, operator, value):
    for attr in vertex.attributes:
        if attr == attribute:
            attribute_value = vertex.attributes[attr].strip()
            if isinstance(value, date):
                try:
                    attribute_value = datetime.strptime(
                        attribute_value, '%Y-%m-%d').date()
                except ValueError:
                    continue
            elif isinstance(value, float):
                try:
                    attribute_value = float(attribute_value)
                except ValueError:
                    continue

            if operator == "=" and value == attribute_value:
                add_vertex(graph, vertex)
                return
            elif operator == ">" and value < attribute_value:
                add_vertex(graph, vertex)
                return
            elif operator == "<" and value > attribute_value:
                add_vertex(graph, vertex)
                return
            elif operator == ">=" and value <= attribute_value:
                add_vertex(graph, vertex)
                return
            elif operator == "<=" and value >= attribute_value:
                add_vertex(graph, vertex)
                return


def parse_query(query):
    attribute = ""
    operator = ""
    value = ""
    operator_list = ["<", ">", "="]
    for c in query:
        if not operator and c not in operator_list:
            attribute += c
        elif c in operator_list:
            operator += c
        else:
            value += c

    attribute = attribute.strip()
    operator = operator.strip()
    new_value = value.strip()

    try:
        new_value = float(value)
    except ValueError:
        pass

    try:
        new_value = datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        pass

    return attribute, operator, new_value


def find_vertex_in_graph(graph, vertex):
    for v in graph.vertices:
        if v.id == vertex.id:
            return v
    return None


def search_vertex(graph, vertex, query):
    for attr in vertex.attributes:
        # print(attr)
        value = vertex.attributes[attr]
        # print(value)
        if (query.lower() in attr.lower()) or (query.lower() in str(value).lower()):
            new_vertex = Vertex(vertex.id)

            new_vertex_found = find_vertex_in_graph(graph, new_vertex)
            if not new_vertex_found:
                new_vertex.attributes.update(vertex.attributes)
            else:
                new_vertex = new_vertex_found

            for e in vertex.edges:
                destination = Vertex(e.destination.id)

                destination_found = find_vertex_in_graph(graph, destination)
                if not destination_found:
                    destination.attributes.update(e.destination.attributes)
                    graph.insert_vertex(destination)
                else:
                    destination = destination_found

                new_vertex.add_edge(
                    Edge(new_vertex, destination, e.relation_name, e.weight, e.is_directed))

            # add if it isn't already added
            if not new_vertex_found:
                graph.insert_vertex(new_vertex)

            return

    for edge in vertex.edges:
        if search_edge(edge, query):
            new_vertex = Vertex(vertex.id)

            new_vertex_found = find_vertex_in_graph(graph, new_vertex)
            if not new_vertex_found:
                new_vertex.attributes.update(vertex.attributes)
            else:
                new_vertex = new_vertex_found

            for e in vertex.edges:
                destination = Vertex(e.destination.id)

                destination_found = find_vertex_in_graph(graph, destination)
                if not destination_found:
                    destination.attributes.update(e.destination.attributes)
                    graph.insert_vertex(destination)
                else:
                    destination = destination_found

                new_vertex.add_edge(
                    Edge(new_vertex, destination, e.relation_name, e.weight, e.is_directed))

            # add if it isn't already added
            if not new_vertex_found:
                graph.insert_vertex(new_vertex)

            return


def search_edge(edge, query):
    relation_name = edge.relation_name
    if relation_name.lower() == query.lower():
        return True


def create_graph(old_graph, graph):
    new_graph = Graph()
    new_graph.vertices.extend(graph.vertices)
    for vertex in old_graph.vertices:
        for edge in vertex.edges:
            destination = find_vertex_in_graph(graph, edge.destination)
            if destination:
                new_vertex = find_vertex_in_graph(graph, vertex)
                if not new_vertex:
                    new_vertex = Vertex(vertex.id)
                    new_vertex.attributes.update(vertex.attributes)
                    new_graph.insert_vertex(new_vertex)
                new_vertex.add_edge(
                    Edge(new_vertex, destination, edge.relation_name, edge.weight, edge.is_directed))
    return new_graph


def complex_visualization(request):
    visualizers = apps.get_app_config('core').visualizers
    graph = apps.get_app_config('core').current_graph

    graph_missing = False
    if graph is None:
        graph_missing = True
    else:
        path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "templates", "mainView.html"))

        for v in visualizers:
            if v.identifier() == "complex-visualizer":
                apps.get_app_config(
                    'core').current_visualizer = "ComplexVisualizer"
                with open(path, 'w') as file:
                    file.write(v.visualize(graph, request))

    # reload_url = reverse('index') + '?reload=true'
    # return redirect(reload_url)
        time.sleep(2)
    
    visualizers = apps.get_app_config('core').visualizers
    loaders = apps.get_app_config('core').loaders
    visualizers = []
    for v in apps.get_app_config('core').visualizers:
        visualizers.append({"name": v.name(), "identifier": v.identifier()})
    loaders = []
    for l in apps.get_app_config('core').loaders:
        loaders.append({"name": l.name(), "identifier": l.identifier()})
    graph = apps.get_app_config('core').current_graph
    tree = apps.get_app_config('core').tree
    return render(request, "index.html", {'graph': graph, 'tree': tree, 'visualizers': visualizers, 'loaders': loaders, "graph_missing": graph_missing})

    return redirect('index')


def simple_visualization(request):
    visualizers = apps.get_app_config('core').visualizers
    graph = apps.get_app_config('core').current_graph
    
    graph_missing = False
    if graph is None:
        graph_missing = True
    else:
        for v in visualizers:
            if v.identifier() == "simple-visualizer":
                apps.get_app_config('core').current_visualizer = "SimpleVisualizer"

                path = os.path.abspath(os.path.join(
                    os.path.dirname(__file__), "templates", "mainView.html"))
                with open(path, 'w') as file:
                    file.write(v.visualize(graph, request))
        time.sleep(2)

    graph = apps.get_app_config('core').current_graph
    tree = apps.get_app_config('core').tree
    visualizers = []
    for v in apps.get_app_config('core').visualizers:
        visualizers.append(
            {"name": v.name(), "identifier": v.identifier()})
    loaders = []
    for l in apps.get_app_config('core').loaders:
        loaders.append(
            {"name": l.name(), "identifier": l.identifier()})
    
    return render(request, "index.html", {"stepper":1, 'graph': graph, 'tree': tree, 'visualizers': visualizers, 'loaders': loaders, 'graph_missing': graph_missing})


def load_relationships_of_vertex(request, id):
    tree = apps.get_app_config('core').tree
    if (id == "favicon.ico"):
        return
    id, option = id.split(";")

    if option == "select":
        if (id.isnumeric()):
            id = int(id)
        node = tree.find_node_by_vertex_id(id)
        node.open()
        node.open_parents()
        tree.last_opened = node.id
        tree_view_html = render_to_string(os.path.abspath(os.path.join(
            os.path.dirname(__file__), "templates", "treeView.html")), {'tree': tree})

        return HttpResponse(tree_view_html)

    elif option == "open":
        node = tree.find_tree_node(int(id))
        if node.opened:
            if len(node.children) != 0:
                node.close()
            if node.parent:
                tree.last_opened = node.parent.id
        else:
            node.open()
            tree.last_opened = node.id

        tree_view_html = render_to_string(os.path.abspath(os.path.join(
            os.path.dirname(__file__), "templates", "treeView.html")), {'tree': tree})

        return HttpResponse(tree_view_html)
    else:
        return redirect("index")
