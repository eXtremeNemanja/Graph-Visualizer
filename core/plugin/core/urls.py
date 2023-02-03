from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('filter', views.filter, name='filter'),
    path('reset', views.reset, name='reset'),
    path('new_data', views.new_data, name='new_data'),
    path('load', views.load, name='load'),
    path('<str:id>', views.load_relationships_of_vertex, name='alter_tree'),
    path('visualizer/<str:type>', views.visualize, name='visualize')
]
