$(document).ready(function(){
    init();
});

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