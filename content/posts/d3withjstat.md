title: D3 and jstat to visualize statistics
date: 2013-09-21
tags: d3, jstat
author: Motoki Wu
summary: R functions are oh so comfortable

R does plotting statistics, well, D3.js does plotting web-friendly interactive plots well. So I decided to weave [jstat](http://www.jstat.org/) (a Javascript stats library) into D3 to plot R-like objects. One of the things people during data analysis is to plot theoretical distributions to check it against the data. In jstat, you can easily do this by doing a ```dnorm``` (for a normal distribution).

	:::javascript
	var range = jstat.seq(-5,5,100);
	var densities = jstat.dnorm(range, 0.0, 1.0);

You can feed this to a "data frame" by using normal Javascript.

	:::javascript
	var dataset = [], zerodata = [];
	for (var i = 0; i < range.length; i++) {
	    dataset.push([range[i], densities[i]]);
	    zerodata.push([0, 0]);
	}

The best feature in D3 is its interpolating algorithm to go from one shape to another. You can create a ```d3.svg.area``` object to define an area from the bottom y = 0, to the top of the distribution. 

	:::javascript
	var pdfArea = d3.svg.area()
	    .x(function(d) { return xscale(d[0]) })
	    .y1(function(d) { return yscale(d[1]) })
	    .y0(h)
	    .interpolate("basis");

Using the populated data frame from above, you can append a ```path``` going from ```zerodata``` (at y = 0) to ```dataset``` (at y = dnorm(x)).

	:::javascript
	svg.append("path")
	    .attr("d", pdfArea(zerodata))
	    .attr("fill", "green")
	    .transition().delay(500).duration(1000)
	    .attr("d", pdfArea(dataset))
	    .attr("fill", d3.rgb(255, 124, 138));

Add some more features like clicking and you get something like this.

<div id="d3">
</div>

Entire code is posted in [bl.ocks](http://bl.ocks.org/tokestermw).

So this example nice, but it's more cosmetic than useful. I'll try a more useful example in the future.

<script type="text/javascript">

var w = 600;
var h = 300;

var svg = d3.select("#d3")
	.append("svg")
    .attr("width", w)
	.attr("height", h);

var xscale = d3.scale.linear()
	.domain([-3, 3])
	.range([0, w]);

var yscale = d3.scale.linear()
	.domain([0, .5])
	.range([h, 0]);
	
var range = jstat.seq(-5,5,100);
var densities = jstat.dnorm(range, 0.0, 1.0);

var dataset = [], zerodata = [];
for (var i = 0; i < range.length; i++) {
	dataset.push([range[i], densities[i]]);
	zerodata.push([0, 0]);
}

var pdfArea = d3.svg.area()
	.x(function(d) { return xscale(d[0]) })
	.y1(function(d) { return yscale(d[1]) })
	.y0(h)
	.interpolate("basis");

var pdfLine = d3.svg.line()
	.x(function(d) { return xscale(d[0])})
	.y(function(d) { return yscale(d[1])})
	.interpolate("basis");

// svg.append("line")
// 	.attr("x1", xscale(d3.min(range)))
// 	.attr("x2", xscale(d3.max(range)))
// 	.attr("y1", h).attr("y2", h)
// 	.attr("stroke-width", 5).attr("stroke", "black");

svg.append("text")
	.attr("dx", 10).attr("dy", 10)
	.attr("width", 30).attr("height", 30)
	.text("click me consecutively");

svg.append("path")
	.attr("d", pdfArea(zerodata))
	.attr("fill", "green")
	.transition().delay(500).duration(1000)
	.attr("d", pdfArea(dataset))
	.attr("fill", d3.rgb(255, 124, 138));

svg.on("click", function() {
	newmean = Math.random() * 6 - 3;
	newden = jstat.dnorm(range, newmean, 1.0);
	var newdata = [];
	for (var i = 0; i < range.length; i++) {
		newdata.push([range[i], newden[i]]);
	}
	svg.select("path")
		.attr("d", pdfArea(zerodata))
		.attr("fill", "pink")
		.transition().delay(500).duration(1000)
		.attr("d", pdfArea(newdata))
		.attr("fill", rgba(255, 124, 138, .5));
})

svg.append("path")
	.attr("d", pdfLine(dataset))
	.attr("stroke", "black")
	.attr("stroke-width", 3)
	.attr("fill", "none");
			
</script>
