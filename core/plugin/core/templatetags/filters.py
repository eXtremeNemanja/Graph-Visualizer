from django import template

register = template.Library()

@register.filter("related_vertices")
def related_vertices(vertex, relationship):
    return vertex.related_vertices(relationship)
