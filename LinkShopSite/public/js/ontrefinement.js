//Setting up the area in the ontology workspace
var areaRefine = d3.select('#ontology_refinement_modal_window');

//Add on the SVG
var svgRefine = areaRefine.append('svg').attr('width','100%').attr('height','75%').attr('style', 'outline: #ccc solid 1px;');

//Defining some variables
var widthRefine;
var node_dataRefine,link_dataRefine;
var linksRefine,nodesRefine;
var offsetRefine;
var radiusRefine;

function displayOntologyRefinementInformation(accuracy, ontology){
  // Update accuracy reading
  console.log(accuracy);
  document.getElementById('ont_refinement_accuracy').innerHTML = accuracy;

  openModal("ontology_refinement");
  ontologyToSvgRefine(ontology);  
}

//Function that takes an ontology dictionary and resets the graph with the new value
function ontologyToSvgRefine(ontology){
  svgRefine.remove();
  //Add on the SVG
  svgRefine = areaRefine.append('svg').attr('width','100%').attr('height','70%').attr('style', 'outline: #ccc solid 1px;');

  //Defining some variables
  widthRefine=parseInt(svgRefine.style('width')),heightRefine=parseInt(svgRefine.style('height'));
  node_dataRefine=[],link_dataRefine=[];
  linksRefine,nodesRefine = null;
  offsetRefine = 5;
  radiusRefine = widthRefine/25;

  var no = [];
  var li = [];
  var keys = Object.keys(ontology);
  for(var i = 0;i<keys.length;i++){ //This is where we 'randomly' place our nodes upon creation.
    var x_pos = 0.2*widthRefine+(i%3)*0.3*widthRefine; //This could serve to be changed.
    var y_pos = 0.2*heightRefine+Math.floor(i/3)*0.3*heightRefine;
    no.push({'name':keys[i],index:i,x:x_pos,y:y_pos});
  }
  node_dataRefine = no;
  for(var i = 0;i<keys.length;i++){
    var ends_list = ontology[keys[i]];
    for(var j = 0;j<ends_list.length;j++){
      var target_index = keys.indexOf(ends_list[j]);
      li.push({source:node_dataRefine[i],target:node_dataRefine[target_index]});
    }
  }
  link_dataRefine = li;
  refreshGraphRefine(node_dataRefine,link_dataRefine);
}

//Function to refresh the graph with new data. Resets the variables, removes
// the old svg elements and replaces them, and adds event handlers
function refreshGraphRefine(nd,li){
  if(nd.length==0) return; //If we don't have any data in the first place, no point in updating
  svgRefine.selectAll('.link').remove();
  svgRefine.selectAll('g').remove();
  linksRefine = svgRefine.selectAll('.link').data(li).enter().append('path').attr('class','link').attr('marker-end', 'url(#arrow)');
  nodesRefine = svgRefine.selectAll('.node').data(nd).enter().append('g');
  nodesRefine.append('circle').attr('class','node').attr('r',radiusRefine);
  nodesRefine.append('text').attr('text-anchor','middle').text(function(d) {return d.name;});
  updateGraphRefine(nd,li);
}

//Function to update the position of the graph based on current data
function updateGraphRefine(nd,li){
  if(nd.length==0) return; //If we don't have any data, no point in updating
  nodesRefine.data(nd).attr('transform',function(d){return "translate("+d.x+","+d.y+")";});
  nodesRefine.selectAll('circle').attr('r',radiusRefine);
  nodesRefine.selectAll('text').each(function(d){
  d3.select(this).attr('font-size',function(d){
    return (3*radiusRefine)/Math.max(2,this.textContent.length) + 'px';
   }).attr('dy','.35em');
  });
  linksRefine.data(li).attr('d', function(d) {
                         var d_x = d.target.x-d.source.x;
                         var d_y = d.target.y-d.source.y;
                         var pathLength = Math.sqrt((d_x*d_x)+(d_y*d_y));
                         if(d.target.x==d.source.x&&d.target.y==d.source.y){
                           var xRotation = -45;
                           var largeArc = 1;               //Here's some annoying math to make sure that the arrowhead
                           var dx = 1/Math.sqrt(2);        //points to the outside of a circle as opposed to the middle
                           var dy = 1/Math.sqrt(2);
                           var new_target_x = d.target.x+(dx*(radiusRefine+offsetRefine));
                           var new_target_y = d.target.y-(dy*(radiusRefine+offsetRefine));
                           var new_start_x = d.source.x-(dx*(radiusRefine));
                           var new_start_y = d.source.y-(dy*(radiusRefine));
                           var dt = radiusRefine;
                           var dt2 = radiusRefine/2;
                           return 'M'+new_start_x+','+new_start_y+'A'+dt+','+dt+' '+xRotation+','+largeArc+','+1+' '+new_target_x+','+new_target_y;
                         } else {
                         d_x = d_x/pathLength;
                         d_y = d_y/pathLength;
                         var new_target_x = d.target.x-(d_x*(radiusRefine+offsetRefine));
                         var new_target_y = d.target.y-(d_y*(radiusRefine+offsetRefine));
                         var dx = new_target_x - d.source.x;
                         var dy = new_target_y - d.source.y;
                         var dr = Math.sqrt(dx*dx+dy*dy);
                         return 'M' + d.source.x+","+d.source.y+"A"+dr+","+dr+" 0 0,1 " + new_target_x + "," + new_target_y;
                         }});
}

function resizeRefine() {
  var temp_coords = [];
  for(var i = 0; i<node_dataRefine.length;i++){
    temp_coords.push({x:(1.0*node_dataRefine[i].x)/widthRefine,y:(1.0*node_dataRefine[i].y)/heightRefine});
  }
  widthRefine=parseInt(svgRefine.style('width'));
  heightRefine=parseInt(svgRefine.style('height'));
  offsetRefine = 5;
  radiusRefine = widthRefine/25;
  for(var i = 0; i<node_dataRefine.length;i++){
    node_dataRefine[i].x=temp_coords[i].x*widthRefine;
    node_dataRefine[i].y=temp_coords[i].y*heightRefine;
  }
  updateGraphRefine(node_dataRefine,link_dataRefine);
}

d3.select(window).on('resize',resizeRefine);