import json;

from plugin.core.services.visualizer import BaseVisualizer
from plugin.core.models import Vertex, Edge, Graph

from django.template import engines

class ComplexVisualizer(BaseVisualizer):
    def identifier(self):
        return "complex-visualizer"

    def name(self):
        return "Complex View"

    def visualize(self, graph, request):
        nodes = {}
        for v in graph.vertices:
            attributes = []
            for attribute_key in v.attributes.keys():
                attributes.append(attribute_key + ": " + str(v.attributes[attribute_key]))
            nodes[v.id] = {
                "id": "ID_" + str(v.id),
                "attributes": attributes
            }
        links = []
        for l in graph.edges():
            link = {"source": l.source.id, "target": l.destination.id}
            links.append(link)

        view = """
                    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

                    <style>
                    .node {
                    cursor: pointer;
                    }

                    .link {
                    fill: none;
                    stroke: #9ecae1;
                    stroke-width: 1.5px;
                    }
                    </style>

                    <script>
                    var current = null;

                    var nodesGraph = JSON.parse("{{nodes |escapejs}}");
                    var linksGraph = JSON.parse("{{links |escapejs}}");

                    linksGraph.forEach(function(link) {
                    link.source = nodesGraph[link.source];
                    link.target = nodesGraph[link.target];
                });
                 d3.select('.stepper').text("1. Please choose a file and then a parser");

                    function nodeClick(el) {

                        var text = "";
                        text += "ID:" + el.id + "\\n";
                        if(current != null) {
                            complexView(nodesGraph[current.id.replace("ID_", "")], '#003B73');
                        }
                        
                        current = el;
                        var node = nodesGraph[el.id.replace("ID_", "")];
                        complexView(node, "red");
                        for(var i=0;i<node.attributes.length;i++) {
                            text += node.attributes[i] + "\\n";
                        }
                        id = el.id.replace("ID_", "");
                        const dynamicTreeContainer = document.getElementById('dynamic-tree');
                        const xhr = new XMLHttpRequest();
                        xhr.open('GET', `/${id};select`, true);
                        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
                        xhr.onreadystatechange = function () {
                            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                                dynamicTreeContainer.innerHTML = xhr.responseText;

                                const newToggles = dynamicTreeContainer.querySelectorAll('.node-toggle');
                                newToggles.forEach(toggle => {
                                    toggle.addEventListener('click', function (event) {
                                        event.preventDefault();
                                        const newNode = this.parentNode;
                                        toggleNode(newNode);
                                    });
                                });
                                if (document.getElementById('last-opened-node') != null) {
                                    const lastOpenedNode = document.getElementById('last-opened-node').innerHTML;
                                    element = document.getElementById(lastOpenedNode);
                                    if (element) {
                                        scrollIfNeeded(element, document.getElementById('tree'));
                                        element.classList.add("selected-item");
                                    }
                                }
                            }
                        };
                        xhr.send();

                        alert(text);
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
                                svg.attr("transform", " translate(" + d3.event.translate + ")" + " scale(" + d3.event.scale + ")")
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
                        d3.selectAll('.node').each(function(d){complexView(d, '#003B73');});

                        function complexView(d, color) {
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
                                .attr('fill', color);

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

                        init();
                
                        function init() {
                            let main = d3.select("#mainView").node();

                            let observer = new MutationObserver(observer_callback);

                            observer.observe(main, {
                                subtree: true,
                                attributes: true,
                                childList: true,
                                characterData: true
                            });
                        }

                        function observer_callback() {
                            let main = d3.select("#mainView").html();
                            d3.select("#birdView").html(main);

                            let mainWidth = d3.select("#mainView").select("g").node().getBBox().width;
                            let mainHeight = d3.select("#mainView").select("g").node().getBBox().height;

                            let birdWidth = $("#birdView")[0].clientWidth;
                            let birdHeight = $("#birdView")[0].clientHeight;

                            let scaleWidth = birdWidth / mainWidth;
                            let scaleHeight = birdHeight / mainHeight;

                            let scale = 0;
                            if(scaleWidth < scaleHeight){
                                scale = scaleWidth;
                            }else{
                                scale = scaleHeight;
                            }
                            
                            let x = d3.select("#birdView").select("g").node().getBBox().x;
                            let y = d3.select("#birdView").select("g").node().getBBox().y;
                            d3.select("#birdView").select('g').attr("transform", "translate ("+[-x*scale, -y*scale]+") scale("+ scale +")");
                        }

                    </script>
                    """


        django_engine = engines['django']
        view_html = django_engine.from_string(view)
        template_html = view_html.render({"nodes": json.dumps(nodes), "links": json.dumps(links)}, request)
        return template_html