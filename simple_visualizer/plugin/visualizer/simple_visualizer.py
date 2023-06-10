import json
from plugin.core.services.visualizer import BaseVisualizer
from django.template import engines

class SimpleVisualizer(BaseVisualizer):

    def identifier(self):
        return "simple-visualizer"

    def name(self):
        return "Simple View"

    def visualize(self, graph, request): 
        vertices = {}
        for v in graph.vertices:
            attributes = []
            for attribute_key in v.attributes.keys():
                attributes.append(attribute_key + ": " + str(v.attributes[attribute_key]))
            vertices[v.id] = {
                "id": "ID_" + str(v.id),
                "attributes": attributes
        }

        links = []
        for e in graph.edges():
            link = {"source": e.source.id, "target": e.destination.id}
            links.append(link)
            

        view = """
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
       
        <style>
        .node {
        cursor: pointer;
        color: #003b73;
        text-align: center;
        }

        .link {
        fill: none;
        stroke: #404040;
        stroke-width: 1.5px;
        }
        </style>

        <script type="text/javascript">

        var current = null;

        var vertices = JSON.parse("{{vertices |escapejs}}");                
        var links= JSON.parse("{{links |escapejs}}");

        links.forEach(function(link) {
            link.source = vertices[link.source];
            link.target = vertices[link.target];
        });

        d3.select('.stepper').text("1. Please choose a file and then a parser");

        var force = d3.layout.force() //kreiranje force layout-a
            .size([1000, 450]) //raspoloziv prostor za iscrtavanje
            .nodes(d3.values(vertices)) //dodaj nodove
            .links(links) //dodaj linkove
            .on("tick", tick) //sta treba da se desi kada su izracunate nove pozicija elemenata
            .linkDistance(25) //razmak izmedju elemenata
            .charge(-450)//koliko da se elementi odbijaju
            .gravity(1)
            .start(); //pokreni izracunavanje pozicija
              
        var svg = d3.select('#mainView').call(d3.behavior.zoom().on("zoom", function () {
                                svg.attr("transform", " translate(" + d3.event.translate + ")" + " scale(" + d3.event.scale + ")")
                        })).append('g');

        // add the links
        var link = svg.selectAll('.link')
            .data(links)
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
        d3.selectAll('.node').each(function(d){simpleView(d, '#003B73');});

        function simpleView(d, color){
            var width=12;
            var textSize=6;

            //Ubacivanje kruga
            d3.select("g#"+d.id).append('circle').
            attr('cx',0).attr('cy', 0).attr('r', width).attr('fill', color);
            //Ubacivanje naziva prodavnice ili artikla
            d3.select("g#"+d.id).append('text').attr('x', 0).attr('y', 4)
            .attr('text-anchor','middle')
            .attr('font-size',textSize).attr('font-family','poppins')
            .attr('fill','white').text(d.id);
        }

        function tick(e) {

            node.attr("transform", function(d) {return "translate(" + d.x + "," + d.y + ")";})
                .call(force.drag);

            link.attr('x1', function(d) { return d.source.x; })
                .attr('y1', function(d) { return d.source.y; })
                .attr('x2', function(d) { return d.target.x; })
                .attr('y2', function(d) { return d.target.y; });

        }
        function nodeClick(el) {

            var text = "";
            text += "ID:" + el.id + "\\n";
            if(current != null) {
                simpleView(vertices[current.id.replace("ID_", "")], '#003B73')
            }
            current = el;
            var node = vertices[el.id.replace("ID_", "")];
            simpleView(node, "red")
            for(var i=0;i<node.attributes.length;i++) {
                text += node.attributes[i] + "\\n";
            }
            alert(text);
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
        view_html = view_html.render({"vertices": json.dumps(vertices), "links":json.dumps(links)}, request)
        return view_html
