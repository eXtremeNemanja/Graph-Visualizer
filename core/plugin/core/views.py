import os
from django.shortcuts import render, redirect
from django.apps.registry import apps
from .models import Edge, Graph, Vertex
from django.template import engines

# Create your views here.
from django.http import HttpResponse


def index(request, file_missing=False):
    print("Log",  "Logging")
    graph = apps.get_app_config('core').base_graph
    tree = apps.get_app_config('core').tree
    return render(request, "index.html", {'graph': graph, 'tree': tree})

def reset(request):
    apps.get_app_config('core').current_graph = apps.get_app_config('core').base_graph
    return redirect('index')

def new_data(request):
    apps.get_app_config('core').base_graph = None
    apps.get_app_config('core').current_graph = None
    return redirect('index')

def load(request):
    choosen_file = None
    if request.method == 'POST' and request.FILES['file']:
        choosen_file = request.FILES['file']
    unique_key = request.POST.get("key")
    loader = apps.get_app_config('core').get_loader(request.POST.get('loader'))
    if not choosen_file:
        return render(request, "index.html", {"file_missing": True})
    else:
        root = loader.load_file(choosen_file, unique_key)
        apps.get_app_config('core').base_graph = loader.make_graph(root)
        apps.get_app_config('core').current_graph = apps.get_app_config('core').base_graph
        apps.get_app_config('core').load_tree()
    return redirect('index')

def search(request, *args, **kwargs):
    # print(args, kwargs)
    query = request.GET.get("query", 'nema')
    if not query:
        return render(request, 'index.html', {'search_error': True, 'graph': apps.get_app_config('core').base_graph})
    
    old_graph = apps.get_app_config('core').current_graph
    graph = Graph()
    for vertex in old_graph.vertices:
        search_vertex(graph, vertex, query)
    
    print(graph)

    apps.get_app_config('core').current_graph = create_graph(old_graph, graph)

    for vertex in apps.get_app_config('core').current_graph.vertices:
        print(vertex.id)
        print(vertex.attributes)
        print(len(vertex.edges))
    return redirect('index')

def filter():
    pass

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
        if (query.lower() in attr.lower()) or (query.lower() in value.lower()):
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
                new_vertex.add_edge(Edge(new_vertex, destination, edge.relation_name, edge.weight, edge.is_directed))
    return new_graph


def complex_visualization(request):
    visualizers = apps.get_app_config('core').visualizers
    for v in visualizers:
        if v.identifier() == "ComplexVisualizer":
            return HttpResponse(
                v.visualize(apps.get_app_config('core').base_graph, request))

    return redirect('index')

def simple_visualization(request):
    visualizers = apps.get_app_config('core').visualizers
    for v in visualizers:
        if v.identifier() == "SimpleVisualizer":
            return HttpResponse(v.visualize(apps.get_app_config('core').base_graph, request))
    return redirect('index')

def load_relationships_of_vertex(request, id):
    print("id", id)
    tree = apps.get_app_config('core').tree
    if (id != 'favicon.ico'):
        vertex = graph.get_vertex_by_id(id)
        vertex.open = not vertex.open
        graph.insert_vertex(vertex)
        apps.get_app_config('core').base_graph = graph
    return redirect('index')
