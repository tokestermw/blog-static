+++
title = "D3 and jstat to visualize statistics"
date = "2013-09-21"
tags = ["d3", "jstat"]
+++

R does plotting statistics well, D3.js does plotting web-friendly interactive plots well. So I decided to weave [jstat](http://www.jstat.org/) (a Javascript stats library) into D3 to plot R-like objects. One of the things people during data analysis is to plot theoretical distributions to check it against the data. In jstat, you can easily do this by using the normal pdf function.

	var range = jStat(jStat.seq(-5,5,100));
	var densities = range.normal(0.0,1.0).pdf()

You can feed this to a "data frame" by using normal Javascript.

	var dataset = [], zerodata = [];
	for (var i = 0; i < range[0].length; i++) {
		dataset.push([range[0][i], densities[0][i]]);
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

	svg.append("path")
	    .attr("d", pdfArea(zerodata))
	    .attr("fill", "green")
	    .transition().delay(500).duration(1000)
	    .attr("d", pdfArea(dataset))
	    .attr("fill", d3.rgb(255, 124, 138));

Add some more features like clicking.

	svg.on("click", function() {
		newmean = Math.random() * 6 - 3;
		newden = range.normal(newmean,1.0).pdf()
		var newdata = [];
		for (var i = 0; i < range[0].length; i++) {
			newdata.push([range[0][i], newden[0][i]]);
		}
		svg.select("path")
			.attr("d", pdfArea(zerodata))
			.attr("fill", "pink")
			.transition().delay(500).duration(1000)
			.attr("d", pdfArea(newdata))
			.attr("fill", d3.rgb(255, 124, 138));
	})

The final result should be in the sidebar.

Entire code is posted in [bl.ocks](http://bl.ocks.org/tokestermw/6652994).
