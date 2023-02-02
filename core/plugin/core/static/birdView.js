$(document).ready(function(){
    init();
});

function init() {
    let mainNode = d3.select("#mainView").node();
    console.log(mainNode);
    let observer = new MutationObserver(observer_callback);

    observer.observe(mainNode, {
        subtree: true,
        attributes: true,
        childList: true,
        characterData: true
    });
}


function observer_callback() {
    let main = d3.select("#mainView").html();
    d3.select("#birdView").html(main); // smestanje html koda iz main u bird view

    let mainWidth = d3.select("#mainView").select("g").node().getBBox().width; // sirina main view-a
    let birdWidth = $("#birdView")[0].clientWidth; // sirina bird view-a

    let mainHeight = d3.select("#mainView").select("g").node().getBBox().height;// visina main view-a
    let birdHeight = $("#birdView")[0].clientHeight; // visina bird view-a

    let scaleWidth = birdWidth / mainWidth;
    let scaleHeight = birdHeight / mainHeight;

    let scale = null; // parametar skaliranja
    if(scaleWidth < scaleHeight){
        scale = scaleWidth;
    }else{
        scale = scaleHeight;
    }
    
    let x = d3.select("#birdView").select("g").node().getBBox().x; // x pozicija g taga unutar svg
    let y = d3.select("#birdView").select("g").node().getBBox().y; // y pozicija g taga unutar svg
    d3.select("#birdView").select('g').attr("transform", "translate ("+[-x*scale, -y*scale]+") scale("+ scale +")");
}