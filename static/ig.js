/*
Uma ferramenta para o apoio na revisão de migração de bases de dados heterogêneas
*/
const width = 600;
const height = 600;
const columns_width = width / 4;
const circle_radius = 7;
const columns_margin = 20;
const columns_space = 60;

const ELEMENTS_LEFT = {};
const ELEMENTS_RIGHT = {};
const EDGES = {};

const edges_size = 3.5;

let element_outer;
let line_outer;
let is_line_outer_visible = false;
let is_tooltip_visible = false;
let svg_click_flag = false;
const debug = false;

function getDataDatabase1(){
    return ["ID", "Name", "Age"];
}

function getDataDatabase2(){
    return ["aluno_id", "idade", "nome", "escola"];
}


function setup(){

    const svg = d3.select("#chart")
    .append("div")
    .classed("svg-container", true) 
    .append("svg")
    .attr("preserveAspectRatio", "xMinYMin meet")
    .attr("viewBox", "0 0 " + width + " " +height)
    .classed("svg-content-responsive", true)
    

    line_outer = svg.append("line")
        .attr("stroke", "#17a2b8")
        .attr("stroke-width", edges_size)
        .attr("x1", 0)
        .attr("y1", 0)
        .attr("x2", 0)
        .attr("y2", 0)

    svg.on("mousemove", function(event) {
        svg_click_flag = true;
        if(is_line_outer_visible){
            let coords = d3.pointer(event);
            line_outer.attr("x1",bound(coords[0], 0, width));
            line_outer.attr("y1",bound(coords[1], 0, height));
        }else{
            line_outer.attr("x1",0);
            line_outer.attr("y1",0);
            line_outer.attr("x2",0);
            line_outer.attr("y2",0);
        }
        //console.log(coords);
    })

    svg.on("click", function(event) {
  
        if(is_tooltip_visible && svg_click_flag){
            hideTooltip()
            svg_click_flag = false;     
        }
        if(is_line_outer_visible && svg_click_flag){
            
            is_line_outer_visible = false;
            svg_click_flag = false;
            line_outer.attr("x1",0);
            line_outer.attr("y1",0);
            line_outer.attr("x2",0);
            line_outer.attr("y2",0);
        }
    })

    if(debug)drawDebugLines(svg);
    
    const columns1 = getDataDatabase1();
    
    let dx = columns_margin;
    let dy = columns_margin;

    for(let i = 0; i < columns1.length; i++){
        console.log(columns1[i]);
        ELEMENTS_LEFT[columns1[i]] = {
            x: dx,
            y: dy,
            text: columns1[i],
            side: "left",
            internal_id: i
        }
        drawElement(svg, ELEMENTS_LEFT[columns1[i]]);
        dy = dy + columns_space;
    }

    const columns2 = getDataDatabase2();
    
    dx = width - columns_width;
    dy = columns_margin;

    for(let i = 0; i < columns2.length; i++){
        console.log(columns2[i]);
        ELEMENTS_LEFT[columns2[i]] = {
            x: dx,
            y: dy,
            text: columns2[i],
            side: "right",
            internal_id: i
        }
        drawElement(svg, ELEMENTS_LEFT[columns2[i]]);
        dy = dy + columns_space;
    }
    
    createtooltip()
}


function drawElement(svg, element){
    if(debug){
        const debug_rect = svg.append("rect")   
        .attr("x", element.x)
        .attr("y", element.y)
        .attr("opacity", 0.5)
        .attr("width", columns_width - columns_margin)
        .attr("height", columns_margin)
        .style("fill", "lightgray")
    }

    const text = svg.append("text")
        .attr("y", element.y + columns_margin/2)
        //.attr("dy", "1em")
        .attr("dy", ".35em")
        .attr("font-size", "15px")
        .attr("font-family", "times")
        .text(element.text)
        if(element.side == "left"){
            text.attr("x", element.x + columns_width  - columns_margin)
            text.attr("text-anchor", "end")
        }else{
            text.attr("text-anchor", "start")
            text.attr("x", element.x)
        }
    
    const circle = svg.append("circle")
        .attr("cy", element.y + columns_margin/2)
        .attr("r", circle_radius)
        .attr("fill", "#17a2b8")
        
        if(element.side == "left"){
            circle.attr("cx", element.x + columns_width - columns_margin + 10)
        }else{
            circle.attr("cx", width - columns_width - 10)
        }

        circle.on("click", function(event) {
            hideTooltip()
            //console.log("CIRCLE CLICKED")
            svg_click_flag = false;
            if(is_line_outer_visible){
                is_line_outer_visible = false;
                
                line_outer.attr("x1",0);
                line_outer.attr("y1",0);
                line_outer.attr("x2",0);
                line_outer.attr("y2",0);
                //NEW EDGE!
                if(element_outer != null){
                    
                    if(element_outer.side != element.side){
                        let left = null;
                        let right = null;

                        if(element_outer.side == "left"){
                            left = element_outer;
                            right = element;
                        }else{
                            left = element;
                            right = element_outer;
                        }   
                        
                        let elementEdge = EDGES[left.internal_id + "$" + right.internal_id] 
                        
                        if(elementEdge == null){
                            
                            const edge = svg.append("line")
                            .attr("stroke", "#17a2b8")
                            .attr("stroke-width", edges_size)
                            .attr("y2", element_outer.y + columns_margin/2)
                            .attr("y1", element.y + columns_margin/2)
                        
                            if(element_outer.side == "left"){
                                edge.attr("x2", element_outer.x + columns_width - columns_margin + 10)
                            }else{ 
                                edge.attr("x2", width - columns_width - 10)
                            }

                            if(element.side == "right"){
                                edge.attr("x1", width - columns_width - 10)
                            }else{ 
                                edge.attr("x1", element.x + columns_width - columns_margin + 10)
                            }

                            EDGES[left.internal_id + "$" + right.internal_id] = {
                                left: left,
                                right: right,
                                edge: edge
                            }
                            
                            edge.on("mouseover", function(event) {
                                edge.attr("stroke-width", edges_size + 3)
                            })
                    
                            edge.on("mouseout", function(event) {
                                edge.attr("stroke-width", edges_size)
                            })

                            edge.on("click", function(event) {
                                console.log("EDGE CLICKED: ", left.text,"<!>", right.text);
                                svg_click_flag = false;
                                showTooltip(EDGES[left.internal_id + "$" + right.internal_id])
                            })
                            
                        }else{
                            console.log("EDGE ALREADY EXISTS")
                        }
                    }
                }
                element_outer = null;
            }else{
                element_outer = element;
                is_line_outer_visible = true;
                let coords = d3.pointer(event);
                line_outer.attr("x1",bound(coords[0], 0, width));
                line_outer.attr("y1",bound(coords[1], 0, height));
                line_outer.attr("x2",bound(coords[0], 0, width));
                line_outer.attr("y2",bound(coords[1], 0, height));
            }
           
        })

        circle.on("mouseover", function(event) {
            d3.select(this).attr('r', circle_radius + 2)
        })

        circle.on("mouseout", function(event) {
           d3.select(this).attr('r', circle_radius)
        })
    
}

function drawDebugLines(svg){
    const opacity = 0.5;
    const strokeWidth = 1;
    
    //CENTER VERTICAL LINE
    svg.append('line')
    .attr("stroke", "green")
    .attr("stroke-width", strokeWidth)
    .attr("opacity", opacity)
    .attr("x1", width/2)
    .attr("y1", 0)
    .attr("x2", width/2)
    .attr("y2", height)
    
    //CENTER HORIZONTAL LINE
    svg.append('line')
    .attr("stroke", "green")
    .attr("stroke-width", strokeWidth)
    .attr("opacity", opacity)
    .attr("x1", 0)
    .attr("y1", height/2)
    .attr("x2", width)
    .attr("y2", height/2)


    //SIDE 1 VERTICAL LINE
    svg.append('line')
    .attr("stroke", "red")
    .attr("stroke-width", strokeWidth)
    .attr("opacity", opacity)
    .attr("x1", columns_width)
    .attr("y1", 0)
    .attr("x2", columns_width)
    .attr("y2", height)

    
    //SIDE 2 VERTICAL LINE
    svg.append('line')
    .attr("stroke", "red")
    .attr("stroke-width", strokeWidth)
    .attr("opacity", opacity)
    .attr("x1", width - columns_width)
    .attr("y1", 0)
    .attr("x2", width - columns_width)
    .attr("y2", height)
    
}

function bound(value, min, max) {
    if (value < min) {
        return min;
    }
    if (value > max) {
        return max;
    }
    return value;
}
setup();



function createtooltip() {
    // d3.select("#tooltip").remove();
    var tooltip = d3.select("#chart")  
        .append("div")
        .classed("col3" ,true)
        .attr("id", "tooltip")

        .classed("hidden", true)
        .style('visibility', "hidden")

        .style("left", "1px")
        .style("top", "0px")
        .style("position", "absolute")
        .style("cursor", "default")
        .style("border-radius","5px")
        .style("background", "white")
        .style("background-position", "left top")
        .style("background-repeat", "repeat")
        .style("padding", "3px")
        // .style("width", width - 5 + "px")
        // .style("height", height/4 + "px")
        .style("border", "2px solid #17a2b8")
        
        tooltip.append("span")
            .text("C1_____")
            .style("font-size","15px")
            .attr("id","C1")
            .style("color","#17a2b8")
            .style("font-weight", "bold")
            .style("padding-right", "10px") 
            
        tooltip.append("span")
            .text("C2_____")
            .attr("id","C2")
            .style("font-size","15px")
            .style("color","#17a2b8")
            .style("font-weight", "bold")
            .style("padding-right", "10px")

        tooltip.append("br")
        tooltip.append("hr").style("border", "1px solid #17a2b8")
        createTooltipMetric(tooltip,"Quant.:")
        createTooltipMetric(tooltip,"Maximo")
        createTooltipMetric(tooltip,"Minimo")
        
        tooltip.append("button")
            .text("Comparar")
            .classed("btn btn-outline-primary btn-sm", true)
            .style("display","block")
            .style("margin","0 auto")
            .style("border-radius","5px")
}   

function createTooltipMetric(tooltip, name){

        tooltip.append("span")
            .text(name)
            .style("font-size","14px")
            .style("color","#17a2b8")
            .style("font-weight", "bold")
            .style("padding-right", "10px") 
        tooltip.append("span")
            .text("0")
            .attr("id",name + "_1")
            .style("font-size","13px")
            .style("color","black")
            .style("padding-right", "30px") 

        tooltip.append("span")
            .text("0")
            .attr("id",name + "_2")
            .style("font-size","13px")
            .style("color","black")
            .style("padding-left", "30px") 
        tooltip.append("span")
            .text(name)
            .style("font-size","14px")
            .style("color","#17a2b8")
            .style("font-weight", "bold")
            .style("padding-left", "10px") 
        tooltip.append("br")
}

function showTooltip(edge_element) {
    const edge = edge_element.edge
    is_tooltip_visible = true;
    const x1 =  parseInt(edge.attr("x1"))
    const y1 =  parseInt(edge.attr("y1"))
    const x2 =  parseInt(edge.attr("x2"))
    const y2 =  parseInt(edge.attr("y2"))
    const x = (x1 + x2) / 2
    const y = (y1 + y2) / 2

    let tooltip = d3.select("#tooltip");
    tooltip.select("#C1").text(edge_element.left.text);
    tooltip.select("#C2").text(edge_element.right.text);

    tooltip
        //.style("border", "2px solid black")
       // .style("left", x + (margin.left - (tooltip.node().getBoundingClientRect().width / 2)) + "px")
        .style("left",  x + "px")
        .style("top",   y + "px")
        .style('visibility', "visible")
        .classed("hidden", false)
    //<button type="button">Click Me!</button>
    

}

function hideTooltip() {
    is_tooltip_visible = false;
    d3.select("#tooltip")
        .classed("hidden", true)
        .style('visibility', "hidden")
}