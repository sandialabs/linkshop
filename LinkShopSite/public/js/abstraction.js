/**
abstraction.js
--------------
Jeffrey Bigg + Scott Watson

Handles visualization of the Abstraction creation tab

Based on "Collapsible Tree" by Mike Bostock
Original: <http://bl.ocks.org/mbostock/4339083>; released under the GNU General Public License, version 3 <https://opensource.org/licenses/GPL-3.0>

**/

/**
Global Code/Initialization
  Global values used by remainder of code and functionality.
  Much of this code is adapted from the cited website.
**/
var absDiv = d3.select('#abstractionEditor').node();
var marginAbs = absDiv.getBoundingClientRect();
var heightAbs = marginAbs.height;
var widthAbs = marginAbs.width;
var iAbs = 0,
    durationAbs = 750,
    rootAbs;

var treeAbs = d3.layout.tree()
    .size([heightAbs, widthAbs]);

var diagonalAbs = d3.svg.diagonal()
    .projection(function(d) { return [d.y, d.x]; });

// Size values
var svgAbs = d3.select('#abstractionEditor').append("svg")
    .attr("width", '100%')
    .attr("height", '98%')
  .append("g")
    //.transform()
    .attr('width','100%')
    .attr('height','98%')
    .attr("transform", "translate(" + (parseInt(marginAbs.left) + 15).toString() + "," + 0 + ")");

var currentRootUpdateElement = null;

/**
absToSvg
  This function is the main entry point for the client receiving 
  abstraction data. It takes the dictionary and displays it. Almost
  all of this code is adapted from the citation. The main modifiable
  values are the size variables.
**/
function absToSvgAbs(abstr){
  rootAbs = transformAbsData(abstr);
  rootAbs = {'name':'commands','children':rootAbs, '_children':null};
  rootAbs.x0 = heightAbs / 2;
  rootAbs.y0 = 0;

  d3.select(self.frameElement).style("height", "400px");

  function collapseAbs(d) {
    if (d.children) {
      d._children = d.children;
      d._children.forEach(collapseAbs);
      d.children = null;
    }
  }

  rootAbs.children.forEach(collapseAbs);
  updateAbs(rootAbs);
  svgToAbstractionAbs();
}

/**
svgToAbstractionAbs
  This function converts the convoluted, redundant SVG data structure
  built from the adapted code back into our JSON structure to be saved at
  the database. 
**/
function svgToAbstractionAbs() {
  return finalAbstractionFix(svgToAbstractionRecursive(rootAbs));
}

/**
svgToAbstractionRecursive
  This is a helper version in the conversion process from SVG back into
  our expected JSON. The main function is to get rid of the shown/hidden
  children aspect of each layer of the tree, and get them into a uniform
  structure. This function performs the first pass over the data, and
  gets the result mostly set up. 
**/
function svgToAbstractionRecursive(absElement) {
    var result = {};
    // root element
    if ((absElement._children === undefined || absElement._children === null) && absElement.children != undefined) {
        for (var i = 0; i < absElement.children.length; i++) {
            result[absElement.children[i].name] = [];

            if ((absElement.children[i]._children === undefined || absElement.children[i]._children === null) && absElement.children[i].children != undefined) {
                for (var j = 0; j < absElement.children[i].children.length; j++) { 
                    if (absElement.children[i].name != "command" || absElement.children[i].name != "arguments")
                      result[absElement.children[i].name].push(svgToAbstractionRecursive(absElement.children[i].children[j]));
                    else
                      result[absElement.children[i].name] = svgToAbstractionRecursive(absElement.children[i].children[j]);
              }
            }
            else if ((absElement.children[i].children === undefined || absElement.children[i].children === null) && (absElement.children[i]._children === undefined || absElement.children[i]._children === null)){
              result = absElement.children[i].name;
              return result;
            } 
            else {

                for (var j = 0; j < absElement.children[i]._children.length; j++) { 
                    if (absElement.children[i].name != "command" || absElement.children[i].name != "arguments")
                      result[absElement.children[i].name].push(svgToAbstractionRecursive(absElement.children[i]._children[j]));
                    else
                      result[absElement.children[i].name] = svgToAbstractionRecursive(absElement.children[i]._children[j]);
              }
            }
        }
    }
    else if ((absElement.children === undefined || absElement.children === null) && (absElement._children === undefined || absElement._children === null)) {
      return;
    } 
    else {
          for (var i = 0; i < absElement._children.length; i++) {
            if (absElement._children[i].name != "command" || absElement._children[i].name != "arguments")
                result[absElement._children[i].name] = [];

            if ((absElement._children[i]._children === undefined || absElement._children[i]._children === null) && absElement._children[i].children != undefined) {
                for (var j = 0; j < absElement._children[i].children.length; j++) { 
                    if (absElement._children[i].name != "command" || absElement._children[i].name != "arguments")
                      result[absElement._children[i].name].push(svgToAbstractionRecursive(absElement._children[i].children[j]));
                    else
                      result[absElement._children[i].name] = svgToAbstractionRecursive(absElement._children[i].children[j]);
              }
            }
            else if ((absElement._children[i].children === undefined || absElement._children[i].children === null) && (absElement._children[i]._children === undefined || absElement._children[i]._children === null)){
              result = absElement._children[i].name;
              return result;
            } 
            else {
                for (var j = 0; j < absElement._children[i]._children.length; j++) { 
                    if (absElement._children[i].name != "command" || absElement._children[i].name != "arguments")
                      result[absElement._children[i].name].push(svgToAbstractionRecursive(absElement._children[i]._children[j]));
                    else
                      result[absElement._children[i].name] = svgToAbstractionRecursive(absElement._children[i]._children[j]);
              }
            }
        }
    }

    return result;
}

/**
finalAbstractionFix
  This is the final pass over the data once it is all exclusively 
  contained in children containers, then the final fixes are applied
  to ensure the data is in the correct format for saving at the 
  database.
**/
function finalAbstractionFix(absOrig) {
  var result = {};

  for (var abs_key in absOrig) {
    curr_abs_commands = []
    for (var i = 0; i < absOrig[abs_key].length; i++) {
      curr_command = { 'expression': absOrig[abs_key][i]['command'][0], 'type': absOrig[abs_key][i]['command'][1] };
      if (absOrig[abs_key][i]['arguments'] !== undefined && absOrig[abs_key][i]['arguments'] !== null) {
        curr_arguments = { 'expression': absOrig[abs_key][i]['arguments'][0], 'type': absOrig[abs_key][i]['arguments'][1] };
        curr_abs_commands.push({ 'command': curr_command, 'arguments': curr_arguments });
      }
      else {
        curr_abs_commands.push({ 'command': curr_command });
      }
    }
    result[abs_key] = curr_abs_commands;
  }
  return result;
}

/**
updateAbs
  This function is responsible for performing the actual graphical 
  update. Almost entirely taken from the cited website.
**/
function updateAbs(source) {

  // Compute the new tree layout.
  var nodesAbs = treeAbs.nodes(rootAbs).reverse(),
      linksAbs = treeAbs.links(nodesAbs);

  // Normalize for fixed-depth.
  nodesAbs.forEach(function(d) { d.y = d.depth * 90; });

  // Update the nodes…
  var nodeAbs = svgAbs.selectAll("g.absNode")
      .data(nodesAbs, function(d) { return d.id || (d.id = ++iAbs); });

  // Enter any new nodes at the parent's previous position.
  var nodeEnterAbs = nodeAbs.enter().append("g")
      .attr("class", "absNode")
      .attr("transform", function(d) { return "translate(" + source.y0 + "," + source.x0 + ")"; })
      .on("click", clickAbs);

  nodeEnterAbs.append("circle")
      .attr("r", 1e-6)
      .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

  nodeEnterAbs.append("text")
      .attr("x", function(d) { return d.children || d._children ? -10 : 10; })
      .attr("dy", ".35em")
      .attr("text-anchor", function(d) { return d.children || d._children ? "end" : "start"; })
      .text(function(d) { return d.name; })
      .style("fill-opacity", 1e-6);

  // Transition nodes to their new position.
  var nodeUpdateAbs = nodeAbs.transition()
      .duration(durationAbs)
      .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });

  nodeUpdateAbs.select("circle")
      .attr("r", 4.5)
      .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

  nodeUpdateAbs.select("text")
      .style("fill-opacity", 1);

  // Transition exiting nodes to the parent's new position.
  var nodeExitAbs = nodeAbs.exit().transition()
      .duration(durationAbs)
      .attr("transform", function(d) { return "translate(" + source.y + "," + source.x + ")"; })
      .remove();

  nodeExitAbs.select("circle")
      .attr("r", 1e-6);

  nodeExitAbs.select("text")
      .style("fill-opacity", 1e-6);

  // Update the links…
  var linkAbs = svgAbs.selectAll("path.absLink")
      .data(linksAbs, function(d) { return d.target.id; });

  // Enter any new links at the parent's previous position.
  linkAbs.enter().insert("path", "g")
      .attr("class", "absLink")
      .attr("d", function(d) {
        var o = {x: source.x0, y: source.y0};
        return diagonalAbs({source: o, target: o});
      });

  // Transition links to their new position.
  linkAbs.transition()
      .duration(durationAbs)
      .attr("d", diagonalAbs);

  // Transition exiting nodes to the parent's new position.
  linkAbs.exit().transition()
      .duration(durationAbs)
      .attr("d", function(d) {
        var o = {x: source.x, y: source.y};
        return diagonalAbs({source: o, target: o});
      })
      .remove();

  // Stash the old positions for transition.
  nodesAbs.forEach(function(d) {
    d.x0 = d.x;
    d.y0 = d.y;
  });
}

/**
expandAllAbs
  Recursively opens all child nodes
**/
function expandAllAbs(d){
  if('children' in d || '_children' in d){
    if(d.children){
    } else {
      d.children = d._children;
      d._children = null;
    }
    for(var i = 0;i<d.children.length;i++){
      expandAllAbs(d.children[i]);
    }
  }
}

/**
detractAllAbs
  Recursively closes all child nodes
**/
function detractAllAbs(d){
  if('children' in d || '_children' in d){
    if(d.children){
      d._children = d.children;
      d.children = null;
    } else {
    }
    for(var i = 0;i<d._children.length;i++){
      detractAllAbs(d._children[i]);
    }
  }
}

/**
transformAbsData
  Takes in the JSON data and recursively formats the object to match 
  the specification of the tree drawing structure.
**/
function transformAbsData(d){
  if(d==null) return;
  if(typeof d == 'object'){
    if(d.constructor === Array){
    var result = [];
    for(var i = 0;i<d.length;i++){
      var da = transformAbsData(d[i]);
      result.push({'name':i.toString(),'children':da,'list':true});
    }
    return result;
  } else {
    var result = [];
    var keys = Object.keys(d);
    for(var i = 0;i<keys.length;i++){
      var da = transformAbsData(d[keys[i]]);
      result.push({'name':keys[i],'children':da,'list':false});
    }
    return result;
  } 
}else {
    return [{'name': d ,'list':false}];
  }
}

/**
clickAbs
  Click handler for nodes. Calls update with the root node
  to expand or detract.
**/
function clickAbs(d) {
  // Expand all
  if(shiftPressed){
    if(d.children){
      detractAllAbs(d);
    } 
    else {
      expandAllAbs(d);
    }
    updateAbs(d);
  }
  // Edit
  else if (ctrlPressed) {
    // Create new abstraction class
    if (d.depth == "0") {
      currentRootUpdateElement = d;
      openModal("new_class");
    }
    // Create new entry for a command
    else if (d.depth == 1) {
      currentRootUpdateElement = d;
      openModal("new_command");
    }
    // Allows editing a command
    else if (d.depth == 2) {
      currentRootUpdateElement = d;
      expandAllAbs(currentRootUpdateElement);
    
      $("[name='edit_command_commandName']").val(currentRootUpdateElement.children[0].children[0].children[0].name);
      $("[name='edit_command_commandType']").val(currentRootUpdateElement.children[0].children[1].children[0].name);
      if (currentRootUpdateElement.children[1]) {
        if (!$('#edit_command_modal_feedback :checkbox').is(':checked')) {
          $('#edit_command_modal_feedback :checkbox').click();
        }
        $("[name='edit_command_commandArgs']").val(currentRootUpdateElement.children[1].children[0].children[0].name);
        $("[name='edit_command_commandArgsType']").val(currentRootUpdateElement.children[0].children[1].children[0].name);
      }
      else {
        if ($('#edit_command_modal_feedback :checkbox').is(':checked')) {
          $('#edit_command_modal_feedback :checkbox').click();
        }
        $("[name='edit_command_commandArgs']").val('');
        $("[name='edit_command_commandArgsType']").val('regEx');
      }

      openModal("edit_command");
    }
  } 
  else if (altPressed) {
    if (d.depth == 1 || (d.depth == 2 && d.parent.children.length > 1) || (d.depth == 3 && d.name == "arguments")) {
      var indexOfDeletion = 0;
      for (var i = 0; i < d.parent.children.length; i++) {
        if (d.parent.children[i].name == d.name) {
          indexOfDeletion = i;
        }
      }
      d.parent.children.splice(indexOfDeletion, 1);

      // Fix names for commands if deleted from middle
      if (d.depth == 2 && (d.parent.children.length != indexOfDeletion)) {
        for (var i = indexOfDeletion; i < d.parent.children.length; i++) {
          d.parent.children[i].name = i.toString();
        }
      }

      for (var i = 0; i < d.parent.children.length; i++) {
        console.log(d.parent.children[i].name);
      }

      updateAbs(d.parent);
    }
  }
  else {
    if (d.children) {
    d._children = d.children;
    d.children = null;
    } 
    else {
    d.children = d._children;
    d._children = null;
  }
  updateAbs(d);
  }
}

function createNewAbstractionClass(absClassName, commandName, commandType, commandArgs, commandArgsType) {

  var expressionText = [{"name":commandName, "list":false}];
  var newExpressionChild = {"name":"expression", "children":expressionText, "list":false};

  var typeText = [{"name":commandType, "list":false}];
  var newTypeChild = {"name":"type", "children":typeText, "list":false};

  var commandArray = [newExpressionChild, newTypeChild];
  var newCommandChild = {"name":"command", "children":commandArray, "list":false};

  var newCommandArgsArray = [newCommandChild];

  if (commandArgs != null) {
    var argsExpressionText = [{"name":commandArgs, "list":false}];
    var argsNewExpressionChild = {"name":"expression", "children":argsExpressionText, "list":false};

    var argsTypeText = [{"name":commandArgsType, "list":false}];
    var argsNewTypeChild = {"name":"type", "children":argsTypeText, "list":false};

    var argsArray = [argsNewExpressionChild, argsNewTypeChild];
    var newArgsChild = {"name":"arguments", "children":argsArray, "list":false};

    newCommandArgsArray.push(newArgsChild);
  }

  var newClassArray = [{"name":"0","children": newCommandArgsArray, "list":true}]

  // Expand if closed
  if (currentRootUpdateElement._children) {
    currentRootUpdateElement.children = currentRootUpdateElement._children;
    currentRootUpdateElement._children = null;
  } 
  currentRootUpdateElement.children.push({'name':absClassName,'children': newClassArray,'list':false});

  updateAbs(currentRootUpdateElement);
}

function createNewAbstractionCommand(commandMode, commandName, commandType, commandArgs, commandArgsType) {
  
  var expressionText = [{"name":commandName, "list":false}];
  var newExpressionChild = {"name":"expression", "children":expressionText, "list":false};

  var typeText = [{"name":commandType, "list":false}];
  var newTypeChild = {"name":"type", "children":typeText, "list":false};

  var commandArray = [newExpressionChild, newTypeChild];
  var newCommandChild = {"name":"command", "children":commandArray, "list":false};

  var newCommandArgsArray = [newCommandChild];

  if (commandArgs != null) {
    var argsExpressionText = [{"name":commandArgs, "list":false}];
    var argsNewExpressionChild = {"name":"expression", "children":argsExpressionText, "list":false};

    var argsTypeText = [{"name":commandArgsType, "list":false}];
    var argsNewTypeChild = {"name":"type", "children":argsTypeText, "list":false};

    var argsArray = [argsNewExpressionChild, argsNewTypeChild];
    var newArgsChild = {"name":"arguments", "children":argsArray, "list":false};

    newCommandArgsArray.push(newArgsChild);
  }

  if (commandMode == 'new') {
    // Expand if closed
    if (currentRootUpdateElement._children) {
      currentRootUpdateElement.children = currentRootUpdateElement._children;
      currentRootUpdateElement._children = null;
    } 
    currentRootUpdateElement.children.push({"name":currentRootUpdateElement.children.length.toString(),"children": newCommandArgsArray, "list":true});
  }
  else {
    var indexOfDeletion = 0;
    for (var i = 0; i < currentRootUpdateElement.parent.children.length; i++) {
      if (currentRootUpdateElement.parent.children[i].name == currentRootUpdateElement.name) {
        indexOfDeletion = i;
      }
    }
    currentRootUpdateElement.parent.children.splice(indexOfDeletion, 1);
    // Fix names for commands if deleted from middle
    if (currentRootUpdateElement.depth == 2 && (currentRootUpdateElement.parent.children.length != indexOfDeletion)) {
      for (var i = indexOfDeletion; i < currentRootUpdateElement.parent.children.length; i++) {
        currentRootUpdateElement.parent.children[i].name = i.toString();
      }
    }

    currentRootUpdateElement.parent.children.push({"name":currentRootUpdateElement.parent.children.length.toString(),"children": newCommandArgsArray, "list":true});

    for (var i = 0; i < currentRootUpdateElement.parent.children.length; i++) {
      console.log(currentRootUpdateElement.parent.children[i].name);
    }

    currentRootUpdateElement = currentRootUpdateElement.parent;

  }

  updateAbs(currentRootUpdateElement);
}

// Code from http://www.the-art-of-web.com/javascript/feedback-modal-window/
// For modal windows

  // Original JavaScript code by Chirp Internet: www.chirp.com.au
// Please acknowledge use of this code by including this header.
function checkNewClassForm () {
    if ($("[name='new_class_absClassName']").val() == '') {
      // Check for redundant name
      createAlert("Please enter a valid name for the new abstraction class.", "Error:", 'danger', 2);
      $("[name='new_class_absClassName']").focus()
      return;
    }
    if ($("[name='new_class_commandName']").val() == '') {
      createAlert("Please enter a valid name for the first command in the new abstraction class.", "Error:", 'danger', 2);
      $("[name='new_class_commandName']").focus()
      return;
    }
    if ($("[name='new_class_commandType']").val() == '') {
      createAlert("Please enter a valid expression for the type specifier of the first command of the new abstraction class.", "Error:", 'danger', 2);
      $("[name='new_class_commandType']").focus()
      return;
    }

    var commandArgs, commandArgsType;

    if($("[name='new_class_addArgList']").is(":checked")) {
      if ($("[name='new_class_commandArgs']").val() == '') {
        createAlert("Please enter a valid expression for the argument list of the first command.", "Error:", 'danger', 2);
        $("[name='new_class_commandArgs']").focus()
        return;
      } 
      commandArgs = $("[name='new_class_commandArgs']").val();
      if ($("[name='new_class_commandArgsType']").val() == '') {
        createAlert("Please enter a valid expression for the type specifier of the argument list of the first command.", "Error:", 'danger', 2);
        $("[name='new_class_commandArgsType']").focus()
        return;
      } 
      commandArgsType = $("[name='new_class_commandArgsType']").val();
    }

    modalWrapper.className = "";
    // CLear form
    createNewAbstractionClass($("[name='new_class_absClassName']").val(), $("[name='new_class_commandName']").val(), $("[name='new_class_commandType']").val(), commandArgs, commandArgsType);

    $("[name='new_class_absClassName']").val('');
    $("[name='new_class_commandName']").val('');
    $("[name='new_class_commandType']").val('regEx');
    $("[name='new_class_commandArgs']").val('');
    $("[name='new_class_commandArgsType']").val('regEx');
  }

  function checkNewCommandForm () {
    if ($("[name='new_command_commandName']").val() == '') {
      createAlert("Please enter a valid name for the command.", "Error:", 'danger', 2);
      $("[name='new_command_commandName']").focus()
      return;
    }
    if ($("[name='new_command_commandType']").val() == '') {
      createAlert("Please enter a valid expression for the type specifier of the command.", "Error:", 'danger', 2);
      $("[name='new_command_commandType']").focus()
      return;
    }

    var commandArgs, commandArgsType;

    if($("[name='new_command_addArgList']").is(":checked")) {
      if ($("[name='new_command_commandArgs']").val() == '') {
        createAlert("Please enter a valid expression for the argument list of the command.", "Error:", 'danger', 2);
        $("[name='new_command_commandArgs']").focus()
        return;
      } 
      commandArgs = $("[name='new_command_commandArgs']").val();
      if ($("[name='new_command_commandArgsType']").val() == '') {
        createAlert("Please enter a valid expression for the type specifier of the argument list of the command.", "Error:", 'danger', 2);
        $("[name='new_command_commandArgsType']").focus()
        return;
      } 
      commandArgsType = $("[name='new_command_commandArgsType']").val();
    }

    modalWrapper.className = "";
    // CLear form
    createNewAbstractionCommand("new", $("[name='new_command_commandName']").val(), $("[name='new_command_commandType']").val(), commandArgs, commandArgsType);

    $("[name='new_command_commandName']").val('');
    $("[name='new_command_commandType']").val('regEx');
    $("[name='new_command_commandArgs']").val('');
    $("[name='new_command_commandArgsType']").val('regEx');
  }

  function checkEditCommandForm () {

    if ($("[name='edit_command_commandName']").val() == '') {
      createAlert("Please enter a valid name for the command.", "Error:", 'danger', 2);
      $("[name='edit_command_commandName']").focus()
      return;
    }
    if ($("[name='edit_command_commandType']").val() == '') {
      createAlert("Please enter a valid expression for the type specifier of the command.", "Error:", 'danger', 2);
      $("[name='edit_command_commandType']").focus()
      return;
    }

    var commandArgs, commandArgsType;

    if($("[name='edit_command_addArgList']").is(":checked")) {
      if ($("[name='edit_command_commandArgs']").val() == '') {
        createAlert("Please enter a valid expression for the argument list of the command.", "Error:", 'danger', 2);
        $("[name='edit_command_commandArgs']").focus()
        return;
      } 
      commandArgs = $("[name='edit_command_commandArgs']").val();
      if ($("[name='edit_command_commandArgsType']").val() == '') {
        createAlert("Please enter a valid expression for the type specifier of the argument list of the command.", "Error:", 'danger', 2);
        $("[name='edit_command_commandArgsType']").focus()
        return;
      } 
      commandArgsType = $("[name='edit_command_commandArgsType']").val();
    }

    modalWrapper.className = "";
    // CLear form
    createNewAbstractionCommand("edit", $("[name='edit_command_commandName']").val(), $("[name='edit_command_commandType']").val(), commandArgs, commandArgsType);

    $("[name='edit_command_commandName']").val('');
    $("[name='edit_command_commandType']").val('regEx');
    $("[name='edit_command_commandArgs']").val('');
    $("[name='edit_command_commandArgsType']").val('regEx');
  }

  var modalWrapper;// = document.getElementById("modal_wrapper");
  var modalWindow;//  = document.getElementById("modal_window");

  function openModal(modal_type)
  {
    if (modal_type == "new_class") {
      modalWrapper = document.getElementById("new_class_modal_wrapper");
      modalWindow  = document.getElementById("new_class_modal_window");
    }
    else if (modal_type == "new_command") {
      modalWrapper = document.getElementById("new_command_modal_wrapper");
      modalWindow  = document.getElementById("new_command_modal_window");
    }
    else if (modal_type == "edit_command") {
      modalWrapper = document.getElementById("edit_command_modal_wrapper");
      modalWindow  = document.getElementById("edit_command_modal_window");
    }
    else if (modal_type == "ontology_refinement") {
      modalWrapper = document.getElementById("ontology_refinement_modal_wrapper");
      modalWindow  = document.getElementById("ontology_refinement_modal_window");
    }

    modalWrapper.className = "overlay";
    modalWindow.style.marginTop = (-modalWindow.offsetHeight)/2 + "px";
    modalWindow.style.marginLeft = (-modalWindow.offsetWidth)/2 + "px";
    //e.preventDefault ? e.preventDefault() : e.returnValue = false;
  };

  var closeModal = function(e)
  {
    modalWrapper.className = "";
    e.preventDefault ? e.preventDefault() : e.returnValue = false;
  };

  var clickHandler = function(e) {
    if(!e.target) e.target = e.srcElement;
    if(e.target.tagName == "DIV") {
      if(e.target.id != "modal_window") closeModal(e);
    }
  };

  var keyHandler = function(e) {
    if(e.keyCode == 27) closeModal(e);
  };

  if(document.addEventListener) {
    //document.getElementById("modal_open").addEventListener("click", openModal, false);
    document.getElementById("new_class_modal_close").addEventListener("click", closeModal, false);
    document.getElementById("new_command_modal_close").addEventListener("click", closeModal, false);
    document.getElementById("edit_command_modal_close").addEventListener("click", closeModal, false);
    document.getElementById("ontology_refinement_modal_close").addEventListener("click", closeModal, false);
    document.addEventListener("click", clickHandler, false);
    document.addEventListener("keydown", keyHandler, false);
  } else {
    //document.getElementById("modal_open").attachEvent("onclick", openModal);
    //document.getElementById("modal_close").attachEvent("onclick", closeModal);
    document.getElementById("new_class_modal_close").attachEvent("onclick", closeModal);
    document.getElementById("new_command_modal_close").attachEvent("onclick", closeModal);
    document.getElementById("edit_command_modal_close").attachEvent("onclick", closeModal);
    document.getElementById("ontology_refinement_modal_close").attachEvent("onclick", closeModal);
    document.attachEvent("onclick", clickHandler);
    document.attachEvent("onkeydown", keyHandler);
  }

  /*
  if(document.addEventListener) {
    document.getElementById("modal_feedback").addEventListener("submit", checkForm, false);
    //document.addEventListener("DOMContentLoaded", modal_init, false);
  } else {
    document.getElementById("modal_feedback").attachEvent("onsubmit", checkForm);
    //window.attachEvent("onload", modal_init);
  }
  */
  $('#new_class_modal_feedback :checkbox').click(function() {
    var $this = $(this);
    // $this will contain a reference to the checkbox   
    if ($this.is(':checked')) {
        // the checkbox was checked 
        $("[name='new_class_commandArgs']").prop("disabled", false);
        $("[name='new_class_commandArgsType']").prop("disabled", false);
    } else {
        // the checkbox was unchecked
        $("[name='new_class_commandArgs']").prop("disabled", true);
        $("[name='new_class_commandArgsType']").prop("disabled", true);
    }
});

  $('#new_command_modal_feedback :checkbox').click(function() {
    var $this = $(this);
    // $this will contain a reference to the checkbox   
    if ($this.is(':checked')) {
        // the checkbox was checked 
        $("[name='new_command_commandArgs']").prop("disabled", false);
        $("[name='new_command_commandArgsType']").prop("disabled", false);
    } else {
        // the checkbox was unchecked
        $("[name='new_command_commandArgs']").prop("disabled", true);
        $("[name='new_command_commandArgsType']").prop("disabled", true);
    }
});

  $('#edit_command_modal_feedback :checkbox').click(function() {
    var $this = $(this);
    // $this will contain a reference to the checkbox   
    if ($this.is(':checked')) {
        // the checkbox was checked 
        $("[name='edit_command_commandArgs']").prop("disabled", false);
        $("[name='edit_command_commandArgsType']").prop("disabled", false);
    } else {
        // the checkbox was unchecked
        $("[name='edit_command_commandArgs']").prop("disabled", true);
        $("[name='edit_command_commandArgsType']").prop("disabled", true);
    }
});

