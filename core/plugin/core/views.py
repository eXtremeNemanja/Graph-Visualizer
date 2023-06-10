from datetime import datetime, date
from django.shortcuts import render, redirect
from django.apps.registry import apps
from .models import Edge, Graph, Vertex
from django.template import engines

# Create your views here.
from django.http import HttpResponse


def index(request, stepper=1,  file_missing=False):
    graph = apps.get_app_config('core').base_graph
    if (graph is not None): stepper = 2
    return render(request, "index.html", {'graph': graph, 'stepper': stepper})
 
def reset(request):
    apps.get_app_config('core').current_graph = apps.get_app_config('core').base_graph
    current_visualizer = apps.get_app_config('core').current_visualizer
    if (current_visualizer == "SimpleVisualizer"):
        return simple_visualization(request)
    elif (current_visualizer == "ComplexVisualizer"):
        return complex_visualization(request)
    else:
        if (apps.get_app_config('core').base_graph is None):
            return render(request, "index.html", {"stepper":1})
        else:
            return render(request, "index.html", {"stepper":2})

def new_data(request):
    apps.get_app_config('core').base_graph = None
    apps.get_app_config('core').current_graph = None
    apps.get_app_config('core').current_visualizer = None
    return redirect('index')

def load(request):
    plugini = apps.get_app_config('core').loaders

    # print(request.FILES)
    # print(request.POST.get('file', 'nema'))
    # print(request.POST.get('loader', 'nema'))
    loader = request.POST.get('loader', 'nema')
    if not request.FILES:
        return render(request, "index.html", {"stepper":1, "file_missing": True})
    else:
        file = request.FILES['file']
        print(file)
        for p in plugini:
            print(p.identifier())
            print(loader)
            if p.identifier() == loader:
                root = p.load_file(file)
                print(root)
                apps.get_app_config('core').base_graph = p.make_graph(root)
                print(apps.get_app_config('core').base_graph)
                apps.get_app_config('core').current_graph = apps.get_app_config('core').base_graph

    # print(file.read())  
    return redirect('index')

def search(request, *args, **kwargs):
    # print(args, kwargs)
    query = request.GET.get("query", 'nema')
    if not apps.get_app_config('core').current_visualizer:
        if apps.get_app_config('core').base_graph is None:
            return render(request, 'index.html', {'search_error': True, 'graph': apps.get_app_config('core').base_graph, 'stepper':1})
        else:
            return render(request, 'index.html', {'search_error': True, 'graph': apps.get_app_config('core').base_graph, 'stepper':2})
    old_graph = apps.get_app_config('core').current_graph
    graph = Graph(old_graph.name)
    for vertex in old_graph.vertices:
        search_vertex(graph, vertex, query)
    
    apps.get_app_config('core').current_graph = create_graph(old_graph, graph)

    current_visualizer = apps.get_app_config('core').current_visualizer
    if (current_visualizer == "SimpleVisualizer"):
        return simple_visualization(request)
    elif (current_visualizer == "ComplexVisualizer"):
        return complex_visualization(request)

def filter(request):
    #todo implement filter
    query = request.GET.get("query", "");
    attribute, operator, value = parse_query(query)
    print(attribute, operator, type(value))
    
    old_graph = apps.get_app_config('core').current_graph
    graph = Graph(old_graph.name)
    for vertex in old_graph.vertices:
        filter_vertex(graph, vertex, attribute, operator, value)

    apps.get_app_config('core').current_graph = create_graph(old_graph, graph)
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

        new_vertex.add_edge(Edge(new_vertex, destination, e.relation_name, e.weight, e.is_directed))
    
    # add if it isn't already added
    if not new_vertex_found:
        graph.insert_vertex(new_vertex)


def filter_vertex(graph, vertex, attribute, operator, value):
    for attr in vertex.attributes:
        if attr == attribute:
            attribute_value = vertex.attributes[attr]
            if isinstance(value, date):
                try:
                    attribute_value = datetime.strptime(attribute_value, '%Y-%m-%d').date()
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
            attribute += c;
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

                new_vertex.add_edge(Edge(new_vertex, destination, e.relation_name, e.weight, e.is_directed))
            
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

                new_vertex.add_edge(Edge(new_vertex, destination, e.relation_name, e.weight, e.is_directed))
            
            # add if it isn't already added
            if not new_vertex_found:
                graph.insert_vertex(new_vertex)
            
            return
        
def search_edge(edge, query):
    relation_name = edge.relation_name
    if relation_name.lower() == query.lower():
        return True
    
def create_graph(old_graph, graph):
    new_graph = Graph(old_graph.name)
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
                new_vertex.add_edge(Edge(new_vertex, destination, edge.relation_name, edge.weight, edge.is_directed))
    return new_graph


def complex_visualization(request):
    visualizers = apps.get_app_config('core').visualizers
    graph = apps.get_app_config('core').current_graph
    if graph is None: return render(request, "index.html", {"stepper":1, "file_missing": False})
    for v in visualizers:
        if v.identifier() == "ComplexVisualizer":
            apps.get_app_config('core').current_visualizer = v.identifier()
            return HttpResponse(
                v.visualize(graph, request))
    return render(request, "index.html", {"stepper":1, "file_missing": False})

def simple_visualization(request):
    visualizers = apps.get_app_config('core').visualizers
    graph = apps.get_app_config('core').current_graph
    if graph is None: 
        return render(request, "index.html", {"stepper":1, "file_missing": False})
    for v in visualizers:
        if v.identifier() == "SimpleVisualizer":
            apps.get_app_config('core').current_visualizer = v.identifier()
            return HttpResponse(v.visualize(graph, request))
    return render(request, "index.html", {"stepper":1, "file_missing": False})
