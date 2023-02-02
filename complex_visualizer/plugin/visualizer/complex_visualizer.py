import json;

from plugin.core.services.visualizer import BaseVisualizer
from plugin.core.models import Vertex, Edge, Graph

from django.template import engines

class ComplexVisualizer(BaseVisualizer):
    def identifier(self):
        return "ComplexVisualizer"

    def name(self):
        return "Show graph with complex view"

    def visualize(self, graph, request):
        nodes = {}
        for v in graph.vertices:
            attributes = []
            for attribute_key in v.attributes.keys():
                attributes.append(attribute_key + ": " + str(v.attributes[attribute_key]))
            nodes[v.id] = {
                "id": "id_" + str(v.id),
                "attributes": attributes
            }
        links = []
        for l in graph.edges():
            link = {"source": l.source.id, "target": l.destination.id}
            links.append(link)

        view = """{% extends "index.html" %}
                    {% block mainView %}
                    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

                    <style>
                    .node {
                    cursor: pointer;
                    color: #003B73;
                    }

                    .link {
                    fill: none;
                    stroke: #9ecae1;
                    stroke-width: 1.5px;
                    }
                    </style>

                    <script>

                    var nodesGraph = JSON.parse("{{nodes |escapejs}}");                
                    var linksGraph = JSON.parse("{{links |escapejs}}");

                    linksGraph.forEach(function(link) {
                    link.source = nodesGraph[link.source];
                    link.target = nodesGraph[link.target];
                });

                    function nodeClick(el){
                        alert("ID: "+el.id);
                        }

                        var force = d3.layout.force() //kreiranje force layout-a
                            .size([1000, 450]) //raspoloziv prostor za iscrtavanje
                            .nodes(d3.values(nodesGraph)) //dodaj nodove
                            .links(linksGraph) //dodaj linkove
                            .on("tick", tick) //sta treba da se desi kada su izracunate nove pozicija elemenata
                            .linkDistance(150) //razmak izmedju elemenata
                            .charge(-1500)//koliko da se elementi odbijaju
                            .gravity(0.75)
                            .start(); //pokreni izracunavanje pozicija

                        // add pan and zoom
                        var svg = d3.select('#mainView').call(d3.behavior.zoom().on("zoom", function () {
                                svg.attr("transform", " scale(" + d3.event.scale + ")")
                        })).append('g');

                        // add the links
                        var link = svg.selectAll('.link')
                            .data(linksGraph)
                            .enter().append('line')
                            .attr('class', 'link');

                        // add the nodes
                        var node = svg.selectAll('.node')
                            .data(force.nodes()) //add
                            .enter().append('g')
                            .attr('class', 'node')
                            .attr('id', function(d){return d.id;})
                            .on('click',function(){
                            nodeClick(this);
                            });
                        d3.selectAll('.node').each(function(d){complexView(d);});

                        function complexView(d) {
                            var length = 10;
                            for(var i=0;i<d.attributes.length;i++) {
                                if(length<d.attributes[i].length) length = d.attributes[i].length
                            }

                            var attributesNum = d.attributes.length;

                            var textSize = 12;
                            var high = 30;
                            high += (attributesNum == 0) ? textSize: attributesNum*textSize;
                            var width = length * textSize/2 + 2*textSize + 5;

                            // add rectangle
                            d3.select("g#"+d.id).append('rect').
                                attr('x',0).attr('y',0).attr('width',width).attr('height',high)
                                .attr('fill','#003B73');

                            // add id
                            d3.select("g#"+d.id).append('text').attr('x',width/2).attr('y',10)
                            .attr('text-anchor','middle')
                            .attr('font-size',textSize).attr('font-family','Poppins')
                            .attr('fill','white').text(d.id);

                            // add divider
                            d3.select("g#"+d.id).append('line').
                            attr('x1',0).attr('y1',textSize).attr('x2',width).attr('y2',textSize)
                            .attr('stroke','gray').attr('stroke-width',2);

                            // add attributes
                            for(var i=0;i<attributesNum;i++)
                            {
                                d3.select("g#"+d.id).append('text').attr('x',0).attr('y',20+i*textSize)
                                .attr('text-anchor','start')
                                .attr('font-size',textSize).attr('font-family','Poppins')
                                .attr('fill','white').text(d.attributes[i]);
                            }
                        }

                        function tick(e) {
                            node.attr("transform", function(d) {return "translate(" + d.x + "," + d.y + ")";})
                                .call(force.drag);

                            link.attr('x1', function(d) { return d.source.x; })
                                .attr('y1', function(d) { return d.source.y; })
                                .attr('x2', function(d) { return d.target.x; })
                                .attr('y2', function(d) { return d.target.y; });
                        }

                    </script>

                    <script  src="static/birdView.js"></script>
                    {% endblock %}"""


        django_engine = engines['django']
        view_html = django_engine.from_string(view)
        template_html = view_html.render({"nodes": json.dumps(nodes), "links": json.dumps(links)}, request)
        return template_html