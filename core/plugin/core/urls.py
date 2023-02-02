from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('reset', views.reset, name='reset'),
    path('new_data', views.new_data, name='new_data'),
    path('load', views.load, name='load'),
    path('search', views.search, name='search'),
    path('<str:id>', views.load_relationships_of_vertex, name='alter_tree'),
    path('simple_visualizer', views.simple_visualization, name='simple_visualizer'),
    path('complex_visualizer', views.complex_visualization, name='complex_visualizer')
]
