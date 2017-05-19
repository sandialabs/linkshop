/** 
linkograph.js
--------
Scott Watson 

File for handling much of the editable nature and display of the linkographs.
**/

// Global Variable delarations and initializations
var linkograph = null; // Current working linkograph
var createSVG = null; // SVG for the create tab
var analyzeSVG = null; // SVG for the analyze tab
var currentObj = null; // Lets you know what node is currently moused over
var selectionColor = '#09f'; // Color for selecttions
var selectedSubLinkLow = null; // Low (numeric) node for selected sub-Linkograph, used in user clicking selection logic
var selectedSubLinkHigh = null; // High (numeric) node for selected sub-Linkograph, used in user clicking selection logic
var redrawSubLinkLow = null; // Low (numeric) node for selected sub-Linkograph, used in redrawing on refresh
var redrawSubLinkHigh = null; // High (numeric) node for selected sub-Linkograph, used in redrawing on refresh
var subLinks = []; // Container for all sublinkographs, shared between this file and the stats JS
var columnWidths = [ 12, 12, 6, 4, 3, 2, 2, 1, 1, 1, 1, 1, 1 ]; // The acceptable column widths for Bootstrap columns on the analyze page
var maxSublinkographs = 8; // The maximum number of sublinkographs which can be displayed on the analyze tab

/**
refreshLinkographs
  Main entry point for displaying a linkograph received from the database 
  at the client
**/
function refreshLinkographs()
{
	if (linkograph != null)
	{
		// Remove linkographs and prepare for redraw
		d3.select('#linkographEditor').remove();

		// Strip the linkograph for analyze tab and/or create page
		var linkographStrippedCommands = stripLinkographCommands();

		// Showing full output with commands
		if (document.getElementById("linkoOutOpt").checked)
        	createSVG = d3.select('#linkographWorkspace').append("div").attr('id', 'linkographEditor').html(linkograph);
		// Strip commands in output
		else
		    createSVG = d3.select('#linkographWorkspace').append("div").attr('id', 'linkographEditor').html(linkographStrippedCommands);

		// Ensure size of full SVG is only as large as the actual Linkograph and grab variables
		createSVG = d3.select('#linkographEditor').select('svg').attr('width', '100%');

		// Remove forward links if specified
		if (!document.getElementById("linkoFlinksOpt").checked)
			createSVG.selectAll("[id*=\"flink\"]").remove();

		// Remove back links if specified
		if (!document.getElementById("linkoBlinksOpt").checked)
			createSVG.selectAll("[id*=\"blink\"]").remove();

		// Add contents of text elements to the value attribute for easier CSS selection
		$("#linkographEditor text").each(function() {
			$(this).attr('value', $(this).text());
    	});

    	// Add click handlers and additional attributes, move circles to front
		createSVG.selectAll("*").on('click',linkoClickHandler);
		createSVG.selectAll("text").attr('class', 'unselectable');
		createSVG.selectAll("circle[id^=\"node\"]").attr('style', 'cursor: pointer;');
		createSVG.selectAll("circle").moveToFront();

		// Reselect sublinkograph if necessary
		if (redrawSubLinkLow != null || redrawSubLinkHigh != null)
			selectSubLinkograph(redrawSubLinkLow, redrawSubLinkHigh);
	}
}

/**
clickHandler
  Function for handling clicking a node on the linkograph, used for
  selecting a starting node and secondary node in sublinkograph
  selection.
**/
function linkoClickHandler() {
  	// Get current id and type information
  	var currId = d3.select(this).attr("id");
  	var currType = getElementType(currId);

	// Logic for selecting a node which can be selected by the circle of via text
	if ((currType == 'node') || (currType == 'text')) {
		// Change currId if selecting a text element
		if (currType == 'text')
			currId = d3.select(this).attr("value");

		var parseNums = currId.match(/[0-9]+/g);
  		var currNum = parseNums[0];

  		// Deselect the initial selection
  		if (selectedSubLinkLow == currNum) {
  			selectedSubLinkLow = null;
  			redrawSubLinkLow = null;
  		}
  		// Handle selecting an initial node
   		//else if ((selectedSubLinkLow == null) || (!shiftPressed)) {
		else if (selectedSubLinkLow == null) {
  			// Initial selection
  			selectedSubLinkLow = currNum;

  			// Reset redraw values
  			redrawSubLinkLow = currNum;
  			redrawSubLinkHigh = null;
  		}
  		// Handle selecting the second node 
  		//else if ((selectedSubLinkLow != null) && (shiftPressed) && (selectedSubLinkLow != currNum))
                else if ((selectedSubLinkLow != null) && (selectedSubLinkLow != currNum))
  		{	
  			// Reorder values in correct order, low is low and high is high
  			if (parseInt(currNum) > parseInt(selectedSubLinkLow))
  				selectedSubLinkHigh = currNum;
  			else {
  				selectedSubLinkHigh = selectedSubLinkLow;
  				selectedSubLinkLow = currNum;
  			}
  		}
  		selectSubLinkograph(selectedSubLinkLow, selectedSubLinkHigh);
  	} 
  	// Case for clicking any other element, should revert all changes
 	else {
  		// Deselect and revert colors
  		// Reset previous colorizations
		createSVG.selectAll(":not(text)").attr('stroke', 'Black').attr('fill', 'Black');
		createSVG.selectAll("text").attr('fill', 'Black');

		// Reset redraw and selection variables
		redrawSubLinkLow = null;
		redrawSubLinkHigh = null;
		selectedSubLinkLow = null;
		selectedSubLinkHigh = null;
  	}
}

/**
selectSubLinkograph
  Function for actually selecting a sublinkograph. Stores the selected
  values and visually displays the actual selection. The low and high 
  variables correspond to the starting and ending indices in the 
  sublinkograph.
**/
function selectSubLinkograph(low, high) {
	// Reset previous colorizations
	createSVG.selectAll(":not(text)").attr('stroke', 'Black').attr('fill', 'Black');
	createSVG.selectAll("text").attr('fill', 'Black');
	if ((low == null) && (high == null)) {
		// Deselecting a node 
	}
	// Handle highlighting just the single node
	else if ((low != null) && (high == null)) {
		// Highlight node
		createSVG.select('#node' + low).moveToFront().attr('stroke', selectionColor).attr('fill',selectionColor);
		createSVG.selectAll('[value^="' + low + ':"]').attr('fill', selectionColor);	
	}
	// Handle selecting a sublinkograph in the specified range
	else {
		createSVG.selectAll(":not(text)").attr('stroke', 'LightGray').attr('fill', 'LightGray');
		createSVG.selectAll("text").attr('fill', 'LightGray');
		//analyzeSVG.selectAll("*").attr("display", "none");

		var intLow = parseInt(low);
		var intHigh = parseInt(high);

		// Highlight all links
		// Loops test for all possible intermediary links, if one is found we perform highlighting
		for (var i = intLow; i < intHigh; i++) {
			for (var j = i + 1; j < intHigh + 1; j++) {
				var currLink = createSVG.select('#' + escapeLeadingNumber(i.toString()) + 'link' + j.toString());
				// Found a link
				if (!currLink.empty()) {
					// Highlight linking edges
					if (document.getElementById("linkoFlinksOpt").checked)
						createSVG.select('#' + escapeLeadingNumber(i.toString()) + 'flink' + j.toString()).moveToFront().attr('stroke', selectionColor);

				  	if (document.getElementById("linkoBlinksOpt").checked)
				  		createSVG.select('#' + escapeLeadingNumber(i.toString()) + 'blink' + j.toString()).moveToFront().attr('stroke', selectionColor);

				  	// Highlight link
					createSVG.select('#' + escapeLeadingNumber(i.toString()) + 'link' + j.toString()).attr('stroke', selectionColor).attr('fill',selectionColor);
				}
			}
		}

		// Highlight and bring all nodes to front
		for (var i = intLow; i <= intHigh; i++) {
			createSVG.select('#node' + i.toString()).attr('stroke', selectionColor).attr('fill',selectionColor);
			createSVG.selectAll('[value^="' + i.toString() + ':"]').attr('fill','black');
		}

		// Reset working values
		// Variables for tracking the user's actual selection
		selectedSubLinkLow = null;
		selectedSubLinkHigh = null;
		// Variables for the actual selected sublinkograph to redraw on refresh
		redrawSubLinkLow = low;
		redrawSubLinkHigh = high;
		// Move circles to front for easy clicking purposes
		createSVG.selectAll("circle").moveToFront();
	}
}

/**
exportSubLinkograph
  Function responsible for drawing the sublinkograph on the analyze tab within
  the column structure and correct output. Low and high correspond to the starting
  and ending indices as well as the user selected name for the linkograph.
**/
function exportSubLinkograph(low, high, name) {
	var numSublinks = subLinks.length;
	var sublinkWorkspace = d3.select("#statsSublinkographs");
	var intLow = parseInt(low);
	var intHigh = parseInt(high);

	// Modify current columns to account for adding a new one
	if (numSublinks > 0) {
		for (var i = 0; i < numSublinks; i++) {
			sublinkWorkspace.select('#statsLinkograph' + i.toString()).attr('class', 'col-sm-' + columnWidths[numSublinks].toString());
		}
	}
	// Create the column
	var currSublinkWorkspace = sublinkWorkspace.append("div")
												.attr('id', 'statsLinkograph' + numSublinks.toString())
												.attr('class', 'col-sm-' + columnWidths[numSublinks].toString())
												.html('<h4>' + name + '</h4>' + '<button id="removeSublink' + numSublinks.toString() + '" class="btn btn-default btn-sm" onclick="removeSublinkograph(this.id)"><span class="glyphicon glyphicon-remove"></span></button>' + stripLinkographCommands() + '<div class=\"row\" id=\"sublinkStats' + numSublinks.toString() + '\"></div>');
	// Add buttons
	//currSublinkWorkspace.append()
	$("#statsLinkograph" + numSublinks.toString() + " text").each(function() {
			$(this).attr('value', $(this).text());
    	});

	// Remove forward links if specified
	if (!document.getElementById("linkoFlinksOpt").checked)
		currSublinkWorkspace.selectAll("[id*=\"flink\"]").remove();

	// Remove back links if specified
	if (!document.getElementById("linkoBlinksOpt").checked)
		currSublinkWorkspace.selectAll("[id*=\"blink\"]").remove();

	// Fix cursor when hovering over text
	currSublinkWorkspace.selectAll("text").attr('class', 'unselectable');

	// Hide all
	currSublinkWorkspace.select("svg").selectAll("*").attr("display", "none");

	// Highlight all links
	// Loops test for all possible intermediary links, if one is found we perform highlighting
	for (var i = intLow; i < intHigh; i++) {
		for (var j = i + 1; j < intHigh + 1; j++) {
			var currLink = createSVG.select('#' + escapeLeadingNumber(i.toString()) + 'link' + j.toString());
			// Found a link
			if (!currLink.empty()) {
				// Highlight linking edges
				if (document.getElementById("linkoFlinksOpt").checked)
					currSublinkWorkspace.select('#' + escapeLeadingNumber(i.toString()) + 'flink' + j.toString()).attr('display', null);
			  	if (document.getElementById("linkoBlinksOpt").checked)
			  		currSublinkWorkspace.select('#' + escapeLeadingNumber(i.toString()) + 'blink' + j.toString()).attr('display', null);

				currSublinkWorkspace.select('#' + escapeLeadingNumber(i.toString()) + 'link' + j.toString()).attr('display', null);
			}
		}
	}

	// Highlight and bring all nodes to front
	for (var i = intLow; i <= intHigh; i++) {
		currSublinkWorkspace.select('#node' + i.toString()).attr('display', null);
		currSublinkWorkspace.selectAll('[value^="' + i.toString() + ':"]').attr('display', null);
	}

	shiftSubLinkograph(low, high, numSublinks);
	currSublinkWorkspace.selectAll('[display=\"none\"]').remove();
	// Shift all the nodes up such that the sublinkograph is properly displayed near the top
	
	// Add current sublinkograph to container
	subLinks.push([low, high, name, $('#linkograph').val(), currSublinkWorkspace.attr('id')]);

	fixSizeSublinksVertical();
	// Fix sizes of sublinkographs
	currSublinkWorkspace.select('svg').attr('width', '100%');
}
	
/**
fixSizeSublinksVertical
  Fixes the height property of the SVG for each linkograph to
  be the height of the tallest sublinkograph. Allows evenly displaying
  despite differently size linkographs.
**/
function fixSizeSublinksVertical() {
	var maxRange = 0;
	var largestLinko = -1;
	var longestText = 0;

	// Find largest ranged linkograph
	for (var l = 0; l < subLinks.length; l++) {
		if ((subLinks[l][1] - subLinks[l][0]) > maxRange) {
			maxRange = subLinks[l][1] - subLinks[l][0];
			largestLinko = l;
		} 
	}

	// Calculate height and update all
	var newHeight = 10 + parseInt(d3.select('#statsLinkograph' + largestLinko.toString()).select('#node' + subLinks[largestLinko][1]).attr('cy'));
	d3.selectAll('[id*=\"statsLinkograph\"]').select('svg').attr('height', newHeight);
}

/**
shiftSubLinkograph
  Logic for shifting the sublinkograph vertically and horizontally, so the sublinkograph
  is correctly sized (reduced in size). x, y values of all elements are hardcoded according 
  to the size of the overall graph, so the sublink must be shifted to be representative of 
  a single graph without lots of arbitrary whitespace. Involves shifting all x, y values of 
  the SVG elements a distance determined by the difference of the closest sublink node from 
  the starting location. Low and high correspond to the initial and ending index of the 
  sublinkograph and the sublinkNum allows for selection of the correct sublink DIV.
**/
function shiftSubLinkograph(low, high, sublinkNum) {
	var intLow = parseInt(low);
	var intHigh = parseInt(high);
	var currSublinkWorkspace = d3.select('#statsLinkograph' + sublinkNum.toString());
	var newY = null;
	var newX = null;
	var shiftX = 0;
	var maxRange = 0;
	var maxLow = 0;
	var maxHigh = 0;
	var maxText = 0;
	var currTextWidth = 0;

	// Shift vertically
	for (var i = intLow; i < intHigh; i++) {
		for (var j = i + 1; j < intHigh + 1; j++) {
			var currLink = currSublinkWorkspace.select('#' + escapeLeadingNumber(i.toString()) + 'link' + j.toString());
			// Found a link
			if (!currLink.empty()) {
				// Shift linking edges
				if (document.getElementById("linkoFlinksOpt").checked) {
					newY = currSublinkWorkspace.select('#' + escapeLeadingNumber(i.toString()) + 'flink' + j.toString()).attr('y1') - (intLow * 20);
					currSublinkWorkspace.select('#' + escapeLeadingNumber(i.toString()) + 'flink' + j.toString()).attr('y1', newY.toString());
					newY = currSublinkWorkspace.select('#' + escapeLeadingNumber(i.toString()) + 'flink' + j.toString()).attr('y2') - (intLow * 20);
					currSublinkWorkspace.select('#' + escapeLeadingNumber(i.toString()) + 'flink' + j.toString()).attr('y2', newY.toString());
				}
			  	if (document.getElementById("linkoBlinksOpt").checked) {
			  		newY = currSublinkWorkspace.select('#' + escapeLeadingNumber(i.toString()) + 'blink' + j.toString()).attr('y1') - (intLow * 20);
					currSublinkWorkspace.select('#' + escapeLeadingNumber(i.toString()) + 'blink' + j.toString()).attr('y1', newY.toString());
					newY = currSublinkWorkspace.select('#' + escapeLeadingNumber(i.toString()) + 'blink' + j.toString()).attr('y2') - (intLow * 20);
					currSublinkWorkspace.select('#' + escapeLeadingNumber(i.toString()) + 'blink' + j.toString()).attr('y2', newY.toString());
			  	}
			  	// Shift link
				newY = currSublinkWorkspace.select('#' + escapeLeadingNumber(i.toString()) + 'link' + j.toString()).attr('cy') - (intLow * 20);
				currSublinkWorkspace.select('#' + escapeLeadingNumber(i.toString()) + 'link' + j.toString()).attr('cy', newY.toString());

				// Determine max range for horizontal shifting
				if ((j-i) > maxRange) {
					maxRange = j - i;
					maxLow = i;
					maxHigh = j;
				}
			}
		}
	}

	// Applies horizontal shift amount based on maximum ranged link
	if (maxHigh != 0)
		shiftX = currSublinkWorkspace.select('#' + escapeLeadingNumber(maxLow.toString()) + 'link' + maxHigh.toString()).attr('cx') - 20;
	else
		shiftX = currSublinkWorkspace.select('#node' + intLow.toString()).attr('cx') - 20;

	// Shift horizontally
	for (var i = intLow; i < intHigh; i++) {
		for (var j = i + 1; j < intHigh + 1; j++) {
			var currLink = currSublinkWorkspace.select('#' + escapeLeadingNumber(i.toString()) + 'link' + j.toString());
			// Found a link
			if (!currLink.empty()) {
				// Shift linking edges
				if (document.getElementById("linkoFlinksOpt").checked) {
					newX = currSublinkWorkspace.select('#' + escapeLeadingNumber(i.toString()) + 'flink' + j.toString()).attr('x1') - shiftX;
					currSublinkWorkspace.select('#' + escapeLeadingNumber(i.toString()) + 'flink' + j.toString()).attr('x1', newX.toString());
					newX = currSublinkWorkspace.select('#' + escapeLeadingNumber(i.toString()) + 'flink' + j.toString()).attr('x2') - shiftX;
					currSublinkWorkspace.select('#' + escapeLeadingNumber(i.toString()) + 'flink' + j.toString()).attr('x2', newX.toString());
				}
			  	if (document.getElementById("linkoBlinksOpt").checked) {
			  		newX = currSublinkWorkspace.select('#' + escapeLeadingNumber(i.toString()) + 'blink' + j.toString()).attr('x1') - shiftX;
					currSublinkWorkspace.select('#' + escapeLeadingNumber(i.toString()) + 'blink' + j.toString()).attr('x1', newX.toString());
					newX = currSublinkWorkspace.select('#' + escapeLeadingNumber(i.toString()) + 'blink' + j.toString()).attr('x2') - shiftX;
					currSublinkWorkspace.select('#' + escapeLeadingNumber(i.toString()) + 'blink' + j.toString()).attr('x2', newX.toString());
			  	}
			  	// Shift link
				newX = currSublinkWorkspace.select('#' + escapeLeadingNumber(i.toString()) + 'link' + j.toString()).attr('cx') - shiftX;
				currSublinkWorkspace.select('#' + escapeLeadingNumber(i.toString()) + 'link' + j.toString()).attr('cx', newX.toString());
			
			}
		}
	}

	// Shift x, y for remaining nodes and text
	for (var i = intLow; i <= intHigh; i++) {
		// New Y value for nodes
		newY = ((i * 20) + 10) - (intLow * 20);
		newX = currSublinkWorkspace.select('#node' + i.toString()).attr('cx') - shiftX;
		currSublinkWorkspace.select('#node' + i.toString()).attr('cy', newY).attr('cx', newX);//.attr('cy', (analyzeSVG.select('#node' + i.toString()).attr('cy') - (20 * intLow)).toString());
		// New Y value for text
		newY += 5;
		newX += 10;
		currSublinkWorkspace.selectAll('[value^="' + i.toString() + ':"]').attr('y', newY).attr('x', newX);

		// Find max text length
		currTextWidth = $('[value^="' + i.toString() + ':"]')[0].getBoundingClientRect().width;
		if (currTextWidth > maxText)
			maxText = currTextWidth;
	}

	// Update parent SVG width
	currSublinkWorkspace.select("svg").attr('width', parseInt(maxText) + parseInt($('[value^="' + intLow.toString() + ':"]')[0].getBoundingClientRect().x) + 10);
}

/**
removeSublinkograph
  Click handler for exporting a currently selected sublinkograph.
**/
function removeSublinkograph(sublinkId) {
	console.log(sublinkId);
	// Grab number of sublink currently clicked to remove
	var currRemoveSublink = sublinkId.match("[0-9]+")[0];
	var sublinkWorkspace = d3.select("#statsSublinkographs");
	var numSublinks = subLinks.length;

	// Remove the sublinkograph 
	sublinkWorkspace.select('#statsLinkograph' + currRemoveSublink).remove();
	subLinks.splice(parseInt(currRemoveSublink), 1);

	for (var i = parseInt(currRemoveSublink); i < numSublinks + 1; i++) {
			sublinkWorkspace.select('#statsLinkograph' + i.toString()).select("button").attr('id', 'removeSublink' + (i-1).toString());
			sublinkWorkspace.select('#statsLinkograph' + i.toString()).attr('id', 'statsLinkograph' + (i-1).toString());
	}
	for (var i = 0; i < numSublinks; i++)
		sublinkWorkspace.select('#statsLinkograph' + i.toString()).attr('class', 'col-sm-' + columnWidths[numSublinks-1].toString());

	console.log(subLinks);
}

/**
addOrRemoveLink
  Click handler for exporting a currently selected sublinkograph.
**/
function addOrRemoveLink(low, high) {
	var linkName = low.toString() + "link" + high.toString();
	var linkSearchPattern = new RegExp('"' + linkName + '"', "i");
	
	if (linkSearchPattern.test(linkograph)) {
		// Link exists, delete

		// Delete link circle
		linkSearchPattern = new RegExp('<circle[\\s]*stroke="[A-Za-z]+"[\\s]*stroke-width="[0-9]+"[\\s]*fill="[A-Za-z]+"[\\s]*cx="[0-9]+"[\\s]*cy="[0-9]+"[\\s]*r="[0-9]+"[\\s]*id="'+linkName+'"[\\s]*\/>', "i");
		linkograph = linkograph.replace(linkSearchPattern, '');
		// Delete flink and blink
		linkName = low.toString() + "flink" + high.toString();
		linkSearchPattern = new RegExp('<line[\\s]*stroke="[A-Za-z]+"[\\s]*stroke-width="[0-9]+"[\\s]*x1="[0-9]+"[\\s]*y1="[0-9]+"[\\s]*x2="[0-9]+"[\\s]*y2="[0-9]+"[\\s]*id="'+linkName+'"[\\s]*\/>', "i");
		linkograph = linkograph.replace(linkSearchPattern, '');
		linkName = low.toString() + "blink" + high.toString();
		linkSearchPattern = new RegExp('<line[\\s]*stroke="[A-Za-z]+"[\\s]*stroke-width="[0-9]+"[\\s]*x1="[0-9]+"[\\s]*y1="[0-9]+"[\\s]*x2="[0-9]+"[\\s]*y2="[0-9]+"[\\s]*id="'+linkName+'"[\\s]*\/>', "i");
		linkograph = linkograph.replace(linkSearchPattern, '');

	}
	else {
		// Link does not exist, create
		console.log("Creating link " + low.toString() + " and " + high.toString());

		newLinkX = createSVG.select('#node' + low.toString()).attr('cx') - ((high - low) * 10);
		newLinkY = ((createSVG.select('#node' + high.toString()).attr('cy') - createSVG.select('#node' + low.toString()).attr('cy'))/2) + parseInt(createSVG.select('#node' + low.toString()).attr('cy'));

		newLinkText = "<circle stroke=\"Black\" stroke-width=\"3\" fill=\"black\" cx=\"" + newLinkX.toString() + "\" cy=\"" + newLinkY.toString() + "\" r=\"3\" id=\"" + linkName.toString() + "\" />\n";
		linkName = low.toString() + "flink" + high.toString();
		newLinkLine1 = "<line stroke=\"black\" stroke-width=\"2\" x1=\"" + createSVG.select('#node' + low.toString()).attr('cx').toString() + "\" y1=\"" + createSVG.select('#node' + low.toString()).attr('cy').toString() + "\" x2=\"" + newLinkX.toString() + "\" y2=\"" + newLinkY.toString() + "\" id=\"" + linkName + "\" />\n";
		linkName = low.toString() + "blink" + high.toString();
		newLinkLine2 = "<line stroke=\"black\" stroke-width=\"2\" x1=\"" + newLinkX.toString() + "\" y1=\"" + newLinkY.toString() + "\" x2=\"" + createSVG.select('#node' + high.toString()).attr('cx').toString() + "\" y2=\"" + createSVG.select('#node' + high.toString()).attr('cy').toString() + "\" id=\"" + linkName + "\" />\n";
		
		updatedLinkograph = linkograph.slice(0, -6) + newLinkText + newLinkLine1 + newLinkLine2 + linkograph.slice(-6);
		linkograph = updatedLinkograph;
	}
	refreshLinkographs();
	convertLinkographSVGtoJSON();
}

/**
convertLinkographSVGtoJSON
  Converts the current working linkograph SVG into an applicable JSON format linkograph
**/
function convertLinkographSVGtoJSON() {
	var lowNodeCounter = 0;
	var highNodeCounter = 0;
	var strippedLinkograph = [];
	while (!createSVG.select('circle[id=\"node'+lowNodeCounter.toString()+'\"]').empty()){
		highNodeCounter = lowNodeCounter + 1;

		var currLinks = [];
		while (!createSVG.select('circle[id=\"node'+highNodeCounter.toString()+'\"]').empty()){
			if (!createSVG.select('line[id=\"'+escapeLeadingNumber(lowNodeCounter.toString())+'flink'+highNodeCounter.toString()+'\"]').empty()) {
				currLinks.push(highNodeCounter);
			}
			highNodeCounter++;
		}
		var addNode = {};
		addNode[getNodeCommandClass(lowNodeCounter)] = currLinks;
		strippedLinkograph.push(addNode);
		lowNodeCounter++;
	}
	
	return strippedLinkograph;
}

function getNodeCommandClass(nodeNum) {
	var linkSearchPattern = new RegExp('>'+nodeNum.toString()+':(.*?)<\/text>', "g");
	var unstrippedText = linkograph.match(linkSearchPattern);
	return unstrippedText[0].slice(unstrippedText[0].indexOf(':')+2, unstrippedText[0].lastIndexOf(','));
}

/**
clickExportLinkograph
  Click handler for exporting a currently selected sublinkograph.
**/
$("#exportLinkograph").click(function() {
	refreshLinkographs();
	var linkographName = prompt('Export Linkograph as', 'sublinkograph' + subLinks.length);
  	if(linkographName==null||linkograph==='') {
  		createAlert("The name of the sublinkograph cannot be empty.", "Error:", "danger", 3);
  		return;
  	}
  	if (redrawSubLinkLow == null || redrawSubLinkHigh == null)
  		createAlert("No sublinkograph is selected.", "Error:", "danger", 3);
  	else if (subLinks.length >= maxSublinkographs) {
  		createAlert("The maximum number of sublinkographs has been reached.", "Error:", "danger", 3);
  	}
  	else {
  		exportSubLinkograph(redrawSubLinkLow, redrawSubLinkHigh, linkographName);
  		createAlert(linkographName + " created on the analyze tab.", "Success!", "success", 3);
  		refreshAllStatistics();
  	}
});

/**
clickAddRemoveLink
  Click handler for adding or removing a selected link for use in ontology refinement.
**/
$("#addRemoveLink").click(function() {
	refreshLinkographs();
  	if (redrawSubLinkLow == null || redrawSubLinkHigh == null)
  		createAlert("No sublinkograph is selected.", "Error:", "danger", 3);
  	else {
  		addOrRemoveLink(redrawSubLinkLow, redrawSubLinkHigh);
  	}
});

/**
moveToFront
  Appends elements to the end, which draws them on top of all other elements and allows
  for easier clicking
**/
d3.selection.prototype.moveToFront = function() {
  return this.each(function(){
    this.parentNode.appendChild(this);
  });
};

/**
escapeLeadingNumber
  Fix for invalid CSS3 IDs which start with numbers
  Adds escape based on unicode: prefix it with \3 and append a space character 
**/
function escapeLeadingNumber(curr) {
	var returnVal = '\\3';
	var numString = curr.toString();
	for (i = 0; i < numString.length; i++) {
		returnVal += numString[i];
		if (i == 0)
			returnVal += ' ';
	}
	return returnVal;
}

/**
getElementType
  Performs regualar expression matching to determine the type of element of the 
  passed in HTML id.
**/
function getElementType(currId) {
	if (currId == null)
		return 'text';
	else if (currId.match(/node[0-9]+/i))
		return 'node';
	else if (currId.match(/[0-9]+link[0-9]+/i))
		return 'link';
	else if (currId.match(/[0-9]+flink[0-9]+/i))
		return 'flink';
	else if (currId.match(/[0-9]+blink[0-9]+/i))
		return 'blink';
	else
		return '0';
}

/**
stripLinkographCommands
  Parses out the data section of a text element starting from the last comma to 
  the last '<' character.
**/
function stripLinkographCommands() {
	return linkograph.replace(/<text\b[^>]*>(.*?)<\/text>/g, function myFunction(x){return x.substr(0, x.lastIndexOf(',')) + x.substr(x.lastIndexOf('<'), x.length);});
}

/**
linkoOutOpt Change Event handler
  Handles the user selecting the linkograph output checkbox, performs full redraw.
**/
$("#linkoOutOpt").change(function(event) {
	refreshLinkographs();
});

/**
linkoFlinksOpt Change Event handler
  Handles the user selecting the display forward links checkbox, performs full redraw.
**/
$("#linkoFlinksOpt").change(function(event) {
	refreshLinkographs();
});

/**
linkoBlinksOpt Change Event handler
  Handles the user selecting the display backward links checkbox, performs full redraw.
**/
$("#linkoBlinksOpt").change(function(event) {
	refreshLinkographs();
});
