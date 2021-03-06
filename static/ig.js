/*
Uma ferramenta para o apoio na revisão de migração de bases de dados heterogêneas
*/
const width = 600;
const height = 600;
const columns_width = width / 4;
const circle_radius = 7;
const columns_margin = 20;
const columns_space = 60;

let ELEMENTS_LEFT = {};
let ELEMENTS_RIGHT = {};
let EDGES = {};
let SQL1 = null;
let SQL2 = null;

const edges_size = 3.5;

let element_outer;
let line_outer;
let is_line_outer_visible = false;
let is_tooltip_visible = false;
let svg_click_flag = false;
const debug = false;

function setup(){

    var editor1 = ace.edit("text_area_1");
    editor1.setTheme("ace/theme/SQL Server");
    editor1.session.setMode("ace/mode/sql");

    var editor2 = ace.edit("text_area_2");
    editor2.setTheme("ace/theme/SQL Server");
    editor2.session.setMode("ace/mode/sql");

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

    d3.select("#button_clean").on("click", function(event) {
        svg.selectAll('*').remove();
        ELEMENTS_LEFT = {};
        ELEMENTS_RIGHT = {};
        EDGES = {};
        element_outer = null;
        line_outer = null;
        is_line_outer_visible = false;
        is_tooltip_visible = false;
        svg_click_flag = false;
    })

   
    d3.select("#button_exec_1").on("click", function(event) {
        const SQL = editor1.getValue()
        console.log("CLICK EXEC 1: " + SQL)
        resetEdgesColor()
        clearSide(svg, 1)
        if(SQL != null){
            SQL1 = SQL;
            requestColumns(svg, 1, SQL)
        }
    })

    d3.select("#button_exec_2").on("click", function(event) {
        const SQL = editor2.getValue()
        console.log("CLICK EXEC 2: " + SQL)
        resetEdgesColor()
        clearSide(svg, 2)
        if(SQL != null){
            SQL2 = SQL;
            requestColumns(svg, 2, SQL)
        }
    })

    if(debug)drawDebugLines(svg);

    d3.select("#table_button").on("click",function(event){
        console.log("Iniciando Comparação de Instâncias")
        d3.select("#table_id").selectAll("*").remove();
        requestAnalysis()
    });   
}

function requestColumns(svg, db, SQL_H) {
    fetch('/api/colunas/'+db, {
        method: 'POST',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ SQL: SQL_H.replaceAll(";", "") })
    }).then(res => res.json())
    .then(function(res){
        if(res.erro != null){
            console.log(res.erro); // ERROR!
            d3.select("#errosql"+db).text(res.erro)
        }else{
            loadColumns(svg, db, res)

        }
    });
}

async function requestCompare(db, SQL_H, value_H) {
    let response = await fetch('/api/generate/'+db, {
        method: 'POST',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
        },
        async: false,
        body: JSON.stringify({ SQL: SQL_H.replaceAll(";", ""), value: "\""+value_H+"\"" })
   
    }).catch(function(err){
        d3.select("#errosql"+db).text(err)
    });
    return response.json();
}

function requestAnalysis(){
    if( Object.keys(EDGES).length > 0){
        let columns1 = []
        let columns2 = []
        let candidate1 = null
        let candidate2 = null
        let candidateFlag = false

        for (x in EDGES) {   
            if(EDGES[x].isCandidate){
                candidateFlag = true;
                candidate1 = EDGES[x].left.text
                candidate2 = EDGES[x].right.text
            }else{
                columns1.push(EDGES[x].left.text);
                columns2.push(EDGES[x].right.text);
            }

        }
        if(candidateFlag){
            fetch('/api/analysis/', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json, text/plain, */*',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(
                { 
                    SQL_1: SQL1.replaceAll(";", ""), 
                    SQL_2: SQL2.replaceAll(";", ""),
                    columns_1: columns1, 
                    columns_2: columns2,
                    candidate_1: candidate1,
                    candidate_2: candidate2
                })
            }).then(res => res.json())
            .then(function(res){
                if(res.erro != null){
                    console.log(res.erro); // ERROR!
                    d3.select("#errosql1").text(res.erro)
                    d3.select("#errosql2").text(res.erro)
                }else{
                    console.log(res)

                    const table = d3.select("#table_id");
                    
                    table.append("th")
                        .attr("class", "table_header")
                        .text(candidate1);

                    for (let i = 0; i < columns1.length; i++) {
                        table.append("th")
                            .attr("class", "table_header")
                            .text(columns1[i]);
                    }

                    table.append("th")
                        .attr("class", "table_header")
                        .text(candidate2);

                    for (let i = 0; i < columns2.length; i++) {
                       table.append("th")
                            .attr("class", "table_header")
                            .text(columns2[i]);
                    }

                    for (let j = 0; j < res.result.length; j++) {  
                        
                        const line = table.append("tr")
                        
                        const c_cell_1 = line.append("td")
                            .attr("class", "table_line")
                        if(res.result[j].t1 == null){
                            c_cell_1.text("Não encontrado")
                        }else{
                            c_cell_1.text(res.result[j].t1[0])
                        }   

                        for (let i = 1; i < columns1.length+1; i++) {
                            const cell = line.append("td")
                                .attr("class", "table_line")
                            if(res.result[j].t1 == null){
                                cell.text("Não encontrado")
                            }else{
                                cell.text(res.result[j].t1[i])
                            }
                        }

                        const c_cell_2 = line.append("td")
                            .attr("class", "table_line")
                        if(res.result[j].t2 == null){
                            c_cell_2.text("Não encontrado")
                        }else{
                            c_cell_2.text(res.result[j].t2[0])
                        }  

                        for (let i = 1; i < columns2.length+1; i++) {
                            const cell = line.append("td")
                                .attr("class", "table_line")
                            if(res.result[j].t2  == null){
                                cell.text("Não encontrado")
                            }else{
                                cell.text(res.result[j].t2[i])
                            }
                        }
                        
                    }

                }
            });
        }
        
    }
}

function clearSide(svg, db){
    hideTooltip()
    if(db == 1){
        for (x in ELEMENTS_LEFT) {   
            ELEMENTS_LEFT[x].circle_g.remove();
            ELEMENTS_LEFT[x].text_g.remove();
        }
        ELEMENTS_LEFT = {};
    }else{
        for (x in ELEMENTS_RIGHT) {   
            ELEMENTS_RIGHT[x].circle_g.remove();
            ELEMENTS_RIGHT[x].text_g.remove();
        }
        ELEMENTS_RIGHT = {};
    }

    //console.log(EDGES)
    for (x in EDGES) {   
        EDGES[x].edge.remove();
    }
    EDGES = {};
}

function loadColumns(svg, db,columns){
    const side = db == 1 ? "left" : "right"
    const elements = db == 1 ? ELEMENTS_LEFT : ELEMENTS_RIGHT;

    let dx = db == 1 ? (columns_margin) : (width - columns_width);
    let dy = columns_margin;

    for(let i = 0; i < columns.length; i++){
        //console.log(columns[i]);
        elements[columns[i]] = {
            x: dx,
            y: dy,
            text: columns[i],
            side: side,
            internal_id: i
        }
        drawElement(svg, elements[columns[i]]);
        dy = dy + columns_space;
    }
    
}


function drawElement(svg, element){

    //console.log(element)
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
        
        element.circle_g = circle
        element.text_g =  text

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
                                console.log("EDGE - CLICKED: ", left.text,"<!>", right.text);
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

function resetEdgesColor(){
    for (x in EDGES) {   
        EDGES[x].edge.attr("stroke", "#17a2b8") //#17a2b8
        EDGES[x].left.circle_g.attr("fill", "#17a2b8")
        EDGES[x].left.text_g.attr("fill", "#17a2b8")
        EDGES[x].right.circle_g.attr("fill", "#17a2b8")
        EDGES[x].right.text_g.attr("fill", "#17a2b8")
        EDGES[x].isCandidate = false
    }
}



function showTooltip(edge_element) {
    const edge = edge_element.edge
    is_tooltip_visible = true;
    /*
    const x1 =  parseInt(edge.attr("x1"))
    const y1 =  parseInt(edge.attr("y1"))
    const x2 =  parseInt(edge.attr("x2"))
    const y2 =  parseInt(edge.attr("y2"))
    const x = (x1 + x2) / 2
    const y = (y1 + y2) / 2
    */
    let tooltip = d3.select("#tooltip");
    tooltip.select("#C1").text(edge_element.left.text);
    tooltip.select("#C2").text(edge_element.right.text);

    if(edge_element.isCandidate){
        tooltip.select("#tooltip_checkbox").property('checked', true);
    }else{
        tooltip.select("#tooltip_checkbox").property('checked', false);
    }
    
    d3.select("#tooltip_button").on("click", function(event) {
        console.log("compare clicked")
        //edge_element
        if(SQL1 != null && SQL2 != null){
            finish_left = false
            finish_right = false

            requestCompare(1,SQL1,edge_element.left.text).then(function(res){
                if(res.erro == null){
                    finish_left = true
                    tooltip.select("#max_1").text(fString(res[0][0]));
                    tooltip.select("#min_1").text(fString(res[0][1]));
                    tooltip.select("#qtd_1").text(fString(res[0][2]));
                    tooltip.select("#avg_1").text(fString(res[0][3]));
                    asynReview(tooltip)
                }else{
                    //console.log(res.erro)
                    d3.select("#errosql1").text(res.erro)
                }
            });

            requestCompare(2,SQL2,edge_element.right.text).then(function(res){
                if(res.erro == null){
                    finish_right = true
                    tooltip.select("#max_2").text(fString(res[0][0]));
                    tooltip.select("#min_2").text(fString(res[0][1]));
                    tooltip.select("#qtd_2").text(fString(res[0][2]));
                    tooltip.select("#avg_2").text(fString(res[0][3]));
                    asynReview(tooltip)
                }else{
                    d3.select("#errosql2").text(res.erro)
                }
            });

        }
    
    })

    tooltip.style('visibility', "visible")
        .classed("hidden", false)

    tooltip.select("#tooltip_checkbox").on("change", function(event){
        resetEdgesColor()
        const selected = d3.select("#tooltip_checkbox").property('checked')
        edge_element.isCandidate = selected
        
        if(edge_element.isCandidate){
            edge_element.edge.attr("stroke", "#F1C40F")
            edge_element.left.circle_g.attr("fill", "#F1C40F")
            edge_element.left.text_g.attr("fill", "#F1C40F")
            edge_element.right.circle_g.attr("fill", "#F1C40F")
            edge_element.right.text_g.attr("fill", "#F1C40F")
        }
        
    }
    );  
    /*
    tooltip.style("left",  x + "px")
        .style("top",   y + "px")
    */
}

let finish_left = false
let finish_right = false

function asynReview(tooltip){
    if(finish_left && finish_right){
        
        
        if( tooltip.select("#max_1").text() ===
            tooltip.select("#max_2").text()){
            console.log("testes")
            tooltip.select("#max_q").style("color","green")
        }else{
            tooltip.select("#max_q").style("color","red")
        }

        if( tooltip.select("#min_1").text() ===
            tooltip.select("#min_2").text()){
            tooltip.select("#min_q").style("color","green")
        }else{
            tooltip.select("#min_q").style("color","red")
        }

        if( tooltip.select("#qtd_1").text() ===
            tooltip.select("#qtd_2").text()){
            tooltip.select("#qtd_q").style("color","green")
        }else{
            tooltip.select("#qtd_q").style("color","red")
        }

        if( tooltip.select("#avg_1").text() ===
            tooltip.select("#avg_2").text()){
            tooltip.select("#avg_q").style("color","green")
        }else{
            tooltip.select("#avg_q").style("color","red")
        }

        finish_left = false
        finish_right = false
    }
}


function hideTooltip() {
    is_tooltip_visible = false;
    const tooltip = d3.select("#tooltip")
        .classed("hidden", true)
        .style('visibility', "hidden")
    
    tooltip.select("#max_1").text("");
    tooltip.select("#min_1").text("");
    tooltip.select("#qtd_1").text("");
    tooltip.select("#avg_1").text("");
    tooltip.select("#max_2").text("");
    tooltip.select("#min_2").text("");
    tooltip.select("#qtd_2").text("");
    tooltip.select("#avg_2").text("");
    tooltip.select("#C1").text("");
    tooltip.select("#C2").text("");

    tooltip.select("#max_q").style("color","#AFCEF5")
    tooltip.select("#min_q").style("color","#AFCEF5")
    tooltip.select("#qtd_q").style("color","#AFCEF5")
    tooltip.select("#avg_q").style("color","#AFCEF5")

    tooltip.select("#tooltip_checkbox").property('checked', false);

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

function fString(s){
    
    if(!isNaN(parseFloat(s))) {
            return "" + parseFloat(s).toFixed(2)   
    }

    const max_s = 10;
    if(s.length >= max_s - 3){
        let new_s = "";
        for (let index = 0; index < max_s - 3; index++) {
            new_s += s.charAt(index)
        }
        new_s += "..." 
        return new_s
    }else{
        return s;
    }
}


setup();