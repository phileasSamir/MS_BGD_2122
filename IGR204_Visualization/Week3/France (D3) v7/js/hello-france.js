// Your code here
// alert("Hello, France!");

const w = 800;
const h = 800;
const h2 = 780;
const w2 = 20;
let dataset = [];
let x = 0;
let y = 0;

//Create SVG element
let svg = d3.select("body")
            .append("svg")
            .attr("width", w)
            .attr("height", h);


// not my code, see https://d3-graph-gallery.com/graph/interactivity_tooltip.html
// create a tooltip
let Tooltip = d3.select("body")
                .append("div")
                .style("opacity", 0)
                .attr("class", "tooltip")
                .style("background-color", "white")
                .style("border", "solid")
                .style("border-width", "2px")
                .style("border-radius", "5px")
                .style("padding", "5px");

// Three function that change the tooltip when user hover / move / leave a cell
let mouseover = function(d) {
                            Tooltip
                            .style("opacity", 1)
                            d3.select(this)
                            .style("stroke", "black")
                            .style("opacity", 1);
                            }

let mousemove = function(d) {
                            Tooltip
                            .text(d.place)
                            .style("left", (d3.pointer(this)[0]+70) + "px")
                            .style("top", (d3.pointer(this)[1]) + "px");
}

let mouseleave = function(d) {
                            Tooltip
                            .style("opacity", 0)
                            d3.select(this)
                            .style("stroke", "none")
                            .style("opacity", 0.8);
}

function draw() {
    svg.selectAll("circle")
        .data(dataset)
        .enter()
        .append("circle")
        .attr("r", (d) => pop(d.population))
        .attr("fill", (d) => d3.interpolateInferno(density(d.density)))
        .attr("cx", (d) => x(d.longitude))
        .attr("cy", (d) => y(d.latitude))
        .attr("opacity", .8)
        .on("mouseover", mouseover)
        .on("mousemove", mousemove)
        .on("mouseleave", mouseleave);
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0, " + h2 + ")")
        .call(d3.axisBottom(x));
    svg.append("g")
        .attr("class", "y axis")
        .attr("transform", "translate(0, " + w2 + ")")
        .call(d3.axisRight(y));
}

d3.tsv("data/france.tsv", (d, i) => {
        return {
            codePostal: +d["Postal Code"],
            inseeCode: +d.inseecode,
            place: d.place,
            longitude: +d.x,
            latitude: +d.y,
            population: +d.population,
            density: +d.density
        };
    }).then( (rows) => {
        console.log(`Loaded ${rows.length} rows.`);
        if (rows.length > 0) {
            console.log("First row: ", rows[0]);
            console.log("Middle row: ", rows[Math.floor(rows.length/2)]);
            console.log("Last row: ", rows[rows.length-1]);
            console.log("Random row: ", rows[Math.floor(Math.random()*rows.length)]);
            dataset = rows; //.slice(0,10);
            x = d3.scaleLinear()
                .domain(d3.extent(rows, (row) => row.longitude))
                .range([50, w-50]);
            y = d3.scaleLinear()
                .domain(d3.extent(rows, (row) => row.latitude))
                .range([h-50, 50]);
            pop = d3.scaleLog() //.scaleLinear to get Corsica back at the cost of having Paris look as big as it should
                .domain([1, d3.max(rows, (row) => row.population)]) //use extent if not using Log scale
                .range([.01,4]);
            density = d3.scaleLinear()
                .domain(d3.extent(rows, (row) => row.density))
                .range([0.1,1]);
            draw();
        }
    }).catch( (error) => {
        console.log("Something went wrong.", error);
    })