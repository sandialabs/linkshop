/** 
stats.js
--------
Scott Watson

Handles creations of Stats objects on the analysis tab

Based on "Collapsible Indented Tree" by Mike Bostock
Original: <http://bl.ocks.org/mbostock/1093025>; released under the GNU General Public License, version 3 <https://opensource.org/licenses/GPL-3.0>

**/

var statsVerticalShift = 10;

/**
statsToSvg
  Main entry point for receiving statistics from the backend, this function takes the dictionary of statistics 
  and updates the corresponding column.
**/
function statsToSvg(stats) {
  for (var i = 0; i < subLinks.length; i++) {
    if (subLinks[i][0] == stats['startRange'] && subLinks[i][1] == stats['stopRange'] && subLinks[i][3] == stats['fileName']) {
      var statsRoot = statsTransformData(stats,stats['startRange']);
      statsRoot = {'name':'Statistics','children':statsRoot};
      statsRoot.x0 = 0;
      statsRoot.y0 = 0;//statsVerticalShift;
      subLinks[i][5] = statsRoot; // Save the 
      statsUpdate(statsRoot, i.toString(), true);
    }
  }
}

/**
statsUpdate
  This function performs the actual drawing of the indented tree structure using D3 based 
  on http://bl.ocks.org/mbostock/1093025. This handles both newly drawing a tree, or updating
  after collapse or expanding. statsRoot is the root node to update from, currStatsLinko is
  the current column handling the sublinkograph, and reset is the flag where true is a fresh
  update (pressed analyze button) and false is an expand/collapse update.
**/
function statsUpdate(statsRoot, currStatsLinko, reset) {
  var iStats = 0,
      statsDuration = 0;

  var statsTree = d3.layout.tree()
      .nodeSize([0, 15]);

  var statsDiagonal = d3.svg.diagonal()
      .projection(function(d) { return [d.y, d.x]; });

  var currStatsDiv;
  var statsSVG;
  
  // Incase of expansd collapse
  if (reset == true) { 
    d3.select('#linkographStats' + currStatsLinko.toString()).remove();
    currStatsDiv = d3.select('#statsLinkograph' + currStatsLinko.toString()).append('div').attr('id', 'linkographStats' + currStatsLinko.toString());
  }
  else {
    currStatsDiv = d3.select('#linkographStats' + currStatsLinko.toString());
  }
  // Grabbing size information and selecting size information for drawing
  var statsMargin = currStatsDiv.node().getBoundingClientRect(),
    statsBarHeight = 15,
    statsBarWidth = 20 + getMaxTextWidth(subLinks[parseInt(currStatsLinko)][5], 0) * 6;

  console.log(statsMargin);

  // Compute the flattened node list. TODO use d3.layout.hierarchy.
  var statsNodes = statsTree.nodes(subLinks[parseInt(currStatsLinko)][5]);

  //var statsHeight = Math.max(500, statsNodes.length * statsBarHeight + statsMargin.statsTop + statsMargin.statsBottom);
  var statsHeight = (statsNodes.length * statsBarHeight) + statsVerticalShift;

  // Create the SVG or select it for update
  if (reset == true) { 
    statsSVG = currStatsDiv.append("svg")
      .attr("width", '100%')
      .attr("height", statsHeight.toString())
    .append("g")
      //.transform()
      .attr('width','100%')
      .attr('height','98%')
      .attr("transform", "translate(" + 0 + "," + statsVerticalShift + ")");
  }
  else {
    statsSVG = currStatsDiv.select('svg').select("g").attr("transform", "translate(" + 0 + "," + statsVerticalShift + ")");
  }

  // The rest of this functions code involves the actual drawing of the tree
  // And is almost entirely copied from the block.org example
  statsSVG.transition()
      .duration(statsDuration)
      .attr("height", statsHeight);

  // Broken TODO
  //currStatsDiv.select(self.frameElement).transition()
    //  .duration(statsDuration)
      //.style("height", statsHeight + "px");

    d3.select(self.frameElement).transition()
      .duration(statsDuration)
      .style("height", statsHeight + "px");

  // Compute the "layout".
  statsNodes.forEach(function(n, i) {
    n.x = (i * statsBarHeight);
  });

  // Update the statsNodes…
  var statsNode = statsSVG.selectAll("g.statsNode")
      .data(statsNodes, function(d) { return d.id || (d.id = ++i); });

  var statsNodeEnter = statsNode.enter().append("g")
      .attr("class", "statsNode")
      .attr("transform", function(d) { return "translate(" + statsRoot.y0 + "," + statsRoot.x0 + ")"; })
      .style("opacity", 1e-6);

  // Enter any new statsNodes at the parent's previous position.
  statsNodeEnter.append("rect")
      .attr("y", (-statsBarHeight / 2))
      .attr("height", statsBarHeight)
      .attr("width", statsBarWidth)
      .style("fill", statsColor)
      .on("click", statsClick);

  statsNodeEnter.append("text")
      .attr("dy", 3.5)
      .attr("dx", 5.5)
      .text(function(d) { return d.name; });

  // Transition statsNodes to their new position.
  statsNodeEnter.transition()
      .duration(statsDuration)
      .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; })
      .style("opacity", 1);

  statsNode.transition()
      .duration(statsDuration)
      .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; })
      .style("opacity", 1)
    .select("rect")
      .style("fill", statsColor);

  // Transition exiting statsNodes to the parent's new position.
  statsNode.exit().transition()
      .duration(statsDuration)
      .attr("transform", function(d) { return "translate(" + statsRoot.y + "," + statsRoot.x + ")"; })
      .style("opacity", 1e-6)
      .remove();

  // Update the links…
  var statsLink = statsSVG.selectAll("path.statsLink")
      .data(statsTree.links(statsNodes), function(d) { return d.target.id; });

  // Enter any new links at the parent's previous position.
  statsLink.enter().insert("path", "g")
      .attr("class", "statsLink")
      .attr("d", function(d) {
        var o = {x: statsRoot.x0, y: statsRoot.y0};
        return d3.svg.diagonal({source: o, target: o});
      })
    .transition()
      .duration(statsDuration)
      .attr("d", statsDiagonal);

  // Transition links to their new position.
  statsLink.transition()
      .duration(statsDuration)
      .attr("d", statsDiagonal);

  // Transition exiting statsNodes to the parent's new position.
  statsLink.exit().transition()
      .duration(statsDuration)
      .attr("d", function(d) {
        var o = {x: statsRoot.x, y: statsRoot.y};
        return d3.svg.diagonal({source: o, target: o});
      })
      .remove();

  // Stash the old positions for transition.
  statsNodes.forEach(function(d) {
    d.x0 = d.x;
    d.y0 = d.y;
  });
}

/**
statsTransformData
  Takes in the JSON data and recursively formats the object to match 
  the specification of the tree drawing structure.
**/
function statsTransformData(d,startRange){
  if(d==null) return;
  if(typeof d == 'object'){
    if(d.constructor === Array){
    var result = [];
    for(var i = 0;i<d.length;i++){
      var da = statsTransformData(d[i],startRange);
      result.push({'name':'Node '+(i+startRange).toString(),'children':da,'list':true});
    }
    return result;
  } else {
    var result = [];
    var keys = Object.keys(d);
    for(var i = 0;i<keys.length;i++){
      var da = statsTransformData(d[keys[i]],startRange);
      result.push({'name':keys[i],'children':da,'list':false});
    }
    return result;
  } 
}else {
    return [{'name': d,'list':false}];
  }
}

/**
getMaxTextWidth
  Get max text width to determine ideal length
**/
function getMaxTextWidth(d, maxText) {
  var textualValue = null;
  if(d.children==null) {
    if (d['name'].toString().length > maxText)
      maxText = d['name'].toString().length;
    return maxText;
  }
  else {
    if (d['name'].length > maxText)
      maxText = d['name'].length;
    for(var i = 0;i<d['children'].length;i++){
      maxText = getMaxTextWidth(d['children'][i], maxText);
    }
    return maxText;
  }
}

/**
statsClick
  Handles clicking a node which performs an update starting from the specified node
  of a specific SVG.
**/
function statsClick(d) {
  if (d.children) {
    d._children = d.children;
    d.children = null;
  } else {
    d.children = d._children;
    d._children = null;
  }

  // Get parent node ID given SVG elements do no have ID's
  var currParent = this.parentNode;
  while (d3.select(currParent).attr('id') == null)
    currParent = currParent.parentNode;

  // Select the actual SVG id to determine the correct SVG to update
  currParent = d3.select(currParent.parentNode).attr('id');

  // Find correct SVG and update
  for (var i = 0; i < subLinks.length; i++) {
    if (subLinks[i][4] == currParent) {
      statsUpdate(d, i, false);
    }
  }
}

/**
refreshAllStatistics
  Sends request and update for all sublinkographs
**/
function refreshAllStatistics() {
  for (var i = 0; i < subLinks.length; i++) {
    performAnalysis(subLinks[i][3], subLinks[i][0], subLinks[i][1]);
  }
}

/**
performAnalysis Button Click Handler
  Sends request for analysis of all sublinkographs to the backend.
**/
$('#performAnalysis').click(function() {
  refreshAllStatistics();
});

/**
statsColor
  Color selector for different nodes
**/
function statsColor(d) {
  return d._children ? "#3182bd" : d.children ? "#c6dbef" : "#998E84";
}
