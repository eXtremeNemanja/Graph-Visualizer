from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.index, name='index'),
    path('filter_search', views.filter_search, name='search'),
    path('load', views.load, name='load'),
    path('reset', views.reset, name='reset'),
    path('new_data', views.new_data, name='new_data'),
    path('simple_visualizer', views.simpleVisualizer, name='simple_visualizer'),
]