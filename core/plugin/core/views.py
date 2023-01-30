from django.shortcuts import render, redirect
from django.apps.registry import apps

from .forms import UploadForm

# Create your views here.
from django.http import HttpResponse


def index(request):
    return render(request, "index.html")

def reset(request):
    apps.get_app_config('core').current_graph = apps.get_app_config('core').base_graph
    return redirect('index')

def new_data(request):
    apps.get_app_config('core').base_graph = None
    apps.get_app_config('core').current_graph = None
    return redirect('index')

def load(request):
    plugini = apps.get_app_config('core').loaders
    
    # print(request.FILES)
    # print(request.POST.get('file', 'nema'))
    # print(request.POST.get('loader', 'nema'))
    loader = request.POST.get('loader', 'nema')
    if not request.FILES:
        print("Nesto")
    else:
        file = request.FILES['file']
        print(file)
        for p in plugini:
            if p.identifier() == loader:
                root = p.load_file(file)
                print(root.tag)
                apps.get_app_config('core').base_graph = p.make_graph(root, root.tag)
                print(apps.get_app_config('core').base_graph)
                apps.get_app_config('core').current_graph = apps.get_app_config('core').base_graph

    # print(file.read())
    # return render(request, "index.html", {"loaders": plugini, "base_graph": apps.get_app_config('core').base_graph})
    return redirect('index')

def filter_search(request, *args, **kwargs):
    print(args, kwargs)
    print(request.method);
    print(request.GET.get('options', 'nema'))
    option = request.GET.get('options', 'nema')
    option_error = False
    if (option == "filter"):
        filter()
    elif (option == "search"):
        search()
    else:
        option_error = True
    # return render(request, "index.html", {"option_error": option_error})
    return redirect('index')

def filter():
    pass

def search():
    pass
