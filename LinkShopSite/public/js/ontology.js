/**
 Author: Jeffrey Bigg
 Note: Some inspiration was driven from the following example (bl.ocks.org/cjrd/6863459)
 Important notice: To prevent overlap in variable naming conventions, all variables and
 functions have the suffix 'Onto' appended. 'Onto' in this case stands for ontology.js.

Based on directed-graph-creator by Colorado Reed
Original: <https://github.com/cjrd/directed-graph-creator>

Copyright (c) 2014 Colorado Reed. Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the .Software.), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED .AS IS., WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

**/

var justiceOnto=false;

//Setting up the area in the ontology workspace
var areaOnto = d3.select('#ontologyWorkspace');

//Add on the SVG
var svgOnto = areaOnto.append('svg').attr('width','100%').attr('height','75%').attr('style', 'outline: #ccc solid 1px;');

//Defining some variables
var widthOnto=parseInt(svgOnto.style('width')),heightOnto=parseInt(svgOnto.style('height'));
var node_dataOnto=[],link_dataOnto=[];
var linksOnto,nodesOnto = null;
var offsetOnto = 5;
var radiusOnto = widthOnto/25;
var currentObjOnto = null; //Lets you know what node is currently moused over
var selectedOnto = false;
var obj1Onto = null; //Selected object
var obj2Onto = null;
var editingOnto = false;
var shiftOnto = false;



//Adding definition for arrowhead
var defsOnto = svgOnto.append('defs');
var markerOnto = defsOnto.append('marker').attr('id','arrow')
                     .attr('viewBox','0 -5 10 10')
                     .attr('refX',6)
                     .attr('markerWidth',6)
                     .attr('markerHeight',6)
                     .attr('orient','auto')
                    .append('path')
                     .attr('d','M0,-5L10,0L0,5')
                     .attr('fill','#000');

//Defining drag behavior for nodes
var dragOnto = d3.behavior.drag()
    .on('drag', function(d) {       
        var nodeOnto = d3.select(this);
        nodeOnto.each(function(d){
                  node_dataOnto[d.index].x = d.x + d3.event.dx;
                  node_dataOnto[d.index].x = Math.max(radiusOnto,node_dataOnto[d.index].x);
                  node_dataOnto[d.index].x = Math.min(widthOnto-radiusOnto,node_dataOnto[d.index].x);
                  node_dataOnto[d.index].y = d.y + d3.event.dy;
                  node_dataOnto[d.index].y = Math.max(radiusOnto,node_dataOnto[d.index].y);
                  node_dataOnto[d.index].y = Math.min(heightOnto-radiusOnto,node_dataOnto[d.index].y);
                  updateGraphOnto(node_dataOnto,link_dataOnto);
                  });
    });


//Function to add a node at a particular x,y coordinate
function addNodeOnto(x,y,name){
  var index = node_dataOnto.length;
  node_dataOnto.push({x:x,y:y,name:name,index:index});
  refreshGraphOnto(node_dataOnto,link_dataOnto);
}

//Function to remove all edges of a node of a particular index
function removeAllEdgesOnto(index){
  for(var i = 0;i<link_dataOnto.length;i++){
    if(link_dataOnto[i].target.index==index || link_dataOnto[i].source.index==index){
      link_dataOnto.splice(i,1);
      removeAllEdgesOnto(index);
      return;
    }
  }
}

//Function to remove the node of a particular index
function removeNodeOnto(index){
 if(index>=0 && index<node_dataOnto.length){
   removeAllEdgesOnto(index);
   for(var i = 0;i<node_dataOnto.length;i++){
     if(i>index){
       node_dataOnto[i].index = i-1;
     }
   }   
   node_dataOnto.splice(index,1);
   refreshGraphOnto(node_dataOnto,link_dataOnto);
 }
}

//Helper function to find the index of a link from the source index
//  to the target index, returning -1 if it isn't found
function indexOfLinkOnto(src,tgt){
  for(var i = 0;i<link_dataOnto.length;i++){
    if(link_dataOnto[i].source.index==src&&link_dataOnto[i].target.index==tgt){
      return i;
    }
  }
  return -1;
}

//Helper function to check for equality of two nodes by comparing their
//  indecies
function nodesEqualOnto(node1,node2){
  node1.each(function(d){
   node2.each(function(d1){
     return d.index==d1.index;
   });
  });
}

//Function to remove an edge from src index to tgt index
function removeEdgeOnto(src,tgt){
  i = indexOfLinkOnto(src,tgt);
  if(i==-1) return;
  link_dataOnto.splice(i,1);
  refreshGraphOnto(node_dataOnto,link_dataOnto);
}

//Function to add an edge from src index to tgt index
function addEdgeOnto(src,tgt){
  if(src>=0 && src<node_dataOnto.length){
    if(tgt>=0 && tgt<node_dataOnto.length){
      if(-1==indexOfLinkOnto(src,tgt)){
        link_dataOnto.push({source: node_dataOnto[src],target: node_dataOnto[tgt]});
        refreshGraphOnto(node_dataOnto,link_dataOnto);
      }
    }
  }
}

//Function to refresh the graph with new data. Resets the variables, removes
// the old svg elements and replaces them, and adds event handlers
function refreshGraphOnto(nd,li){
  if(nd.length==0) return; //If we don't have any data in the first place, no point in updating
  saveEditsOnto();
  currentObjOnto = null;
  selectedOnto = false;
  obj1Onto = null;
  obj2Onto = null;
  editingOnto = false;
  shiftOnto = false;
  currentStringOnto = "";
  svgOnto.selectAll('.link').remove();
  svgOnto.selectAll('g').remove();
  linksOnto = svgOnto.selectAll('.link').data(li).enter().append('path').attr('class','link').attr('marker-end', 'url(#arrow)');
  nodesOnto = svgOnto.selectAll('.node').data(nd).enter().append('g');
  nodesOnto.append('circle').attr('class','node').attr('r',radiusOnto);
  nodesOnto.append('text').attr('text-anchor','middle').text(function(d) {return d.name;});
  updateGraphOnto(nd,li);
  dragOnto.call(nodesOnto);
  nodesOnto.on('mouseover',onMouseoverOnto);
  nodesOnto.on('mouseout',onMouseoutOnto);
}

//Function to update the position of the graph based on current data
function updateGraphOnto(nd,li){
  if(nd.length==0) return; //If we don't have any data, no point in updating
  nodesOnto.data(nd).attr('transform',function(d){return "translate("+d.x+","+d.y+")";});
  nodesOnto.selectAll('circle').attr('r',radiusOnto);
  nodesOnto.selectAll('text').each(function(d){
  d3.select(this).attr('font-size',function(d){
    return (3*radiusOnto)/Math.max(2,this.textContent.length) + 'px';
   }).attr('dy','.35em');
  });
  linksOnto.data(li).attr('d', function(d) {
                         var d_x = d.target.x-d.source.x;
                         var d_y = d.target.y-d.source.y;
                         var pathLength = Math.sqrt((d_x*d_x)+(d_y*d_y));
                         if(d.target.x==d.source.x&&d.target.y==d.source.y){
                           var xRotation = -45;
                           var largeArc = 1;               //Here's some annoying math to make sure that the arrowhead
                           var dx = 1/Math.sqrt(2);        //points to the outside of a circle as opposed to the middle
                           var dy = 1/Math.sqrt(2);
                           var new_target_x = d.target.x+(dx*(radiusOnto+offsetOnto));
                           var new_target_y = d.target.y-(dy*(radiusOnto+offsetOnto));
                           var new_start_x = d.source.x-(dx*(radiusOnto));
                           var new_start_y = d.source.y-(dy*(radiusOnto));
                           var dt = radiusOnto;
                           var dt2 = radiusOnto/2;
                           return 'M'+new_start_x+','+new_start_y+'A'+dt+','+dt+' '+xRotation+','+largeArc+','+1+' '+new_target_x+','+new_target_y;
                         } else {
                         d_x = d_x/pathLength;
                         d_y = d_y/pathLength;
                         var new_target_x = d.target.x-(d_x*(radiusOnto+offsetOnto));
                         var new_target_y = d.target.y-(d_y*(radiusOnto+offsetOnto));
                         var dx = new_target_x - d.source.x;
                         var dy = new_target_y - d.source.y;
                         var dr = Math.sqrt(dx*dx+dy*dy);
                         return 'M' + d.source.x+","+d.source.y+"A"+dr+","+dr+" 0 0,1 " + new_target_x + "," + new_target_y;
                         }});
}

//Click handler for svg to handle selection, node creation, and edge toggling
svgOnto.on('click',function(d){
       var coords = d3.mouse(this);
       var x = coords[0];
       var y = coords[1];
       var name = "Node "+(node_dataOnto.length+1);
       if(d3.event.shiftKey&&currentObjOnto==null&&obj1Onto==null){
         addNodeOnto(x,y,name);
       }
       if(d3.event.shiftKey&&currentObjOnto!=null){
         if(obj1Onto==null){
           obj1Onto = currentObjOnto;
           obj1Onto.select('circle').style('fill','#69f');
           selectedOnto=true;
         } else if (obj2Onto==null){
           obj2Onto = currentObjOnto;
           obj1Onto.each(function(d){
             obj2Onto.each(function(d1){
               if(d.index==d1.index){
                 obj1Onto.select('circle').style('fill','#ccc');
               }else{
                 if(-1==indexOfLinkOnto(d.index,d1.index)){
                   addEdgeOnto(d.index,d1.index);
                 }else{
                   removeEdgeOnto(d.index,d1.index);
                 }
               }
             });
           });
           obj1Onto=null;
           obj2Onto=null;
           selectedOnto=false;
         }
       }
     });
//Sets the key press handlers
d3.select('body').on('keydown',onKeyDownOnto).on('keyup',onKeyUpOnto);

//Key press handler for a key down press. It is here where self links, node
// editing, and node deleting is handled.
//Since this gets saved eventually as a JSON string, it might not be a good
//idea to allow for the characters ' " [] {} as those are control characters.
//Further note: This is a key press handler for the 'body' DOM element. stats.py
//also has a key press handler. It might be worthwhile to combine these key press
//handlers together to avoid any confusion.
function onKeyDownOnto(){
  if(obj1Onto!=null){
  if(d3.event.ctrlKey){//Self loop creation
    var node = obj1Onto;
    node.each(function(d){
      if(-1==indexOfLinkOnto(d.index,d.index)){
        addEdgeOnto(d.index,d.index);
      } else {
        removeEdgeOnto(d.index,d.index);
      }
    });
  }
  if(d3.event.keyCode==16){//shift key is pressed
    shiftOnto = true;
  }
  if(d3.event.keyCode==32){//space key is pressed
    if(editingOnto){
      d3.event.preventDefault();
      currentStringOnto+=' ';
      obj1Onto.select('text').text(currentStringOnto);
      updateGraphOnto(node_dataOnto,link_dataOnto);
    }
  }
  if(d3.event.keyCode==190){//This is a period piece
    if(editingOnto){
      if(shiftOnto){
        currentStringOnto+='>';
      } else {
        currentStringOnto+='.';
      }
      obj1Onto.select('text').text(currentStringOnto);
      updateGraphOnto(node_dataOnto,link_dataOnto);
    }
  }
  if(d3.event.keyCode==188){//This handles commas
    if(editingOnto){
      if(shiftOnto){
        currentStringOnto+='<';
      } else {
        currentStringOnto+=',';
      }
      obj1Onto.select('text').text(currentStringOnto);
      updateGraphOnto(node_dataOnto,link_dataOnto);
    }
  }
  if(d3.event.keyCode==191){//This handles questions.
    if(editingOnto){            //But only the question mark key.
      if(shiftOnto){            //For actual answers, talk to 
        currentStringOnto+='?'; //whomever is currently maintaining
      } else {                  //this project.
        d3.event.preventDefault();
        currentStringOnto+='/';
      }
      obj1Onto.select('text').text(currentStringOnto);
      updateGraphOnto(node_dataOnto,link_dataOnto);
    }
  }
  if(d3.event.keyCode>=65&&d3.event.keyCode<=90){//letter key is pressed
    if(editingOnto){
      d3.event.preventDefault();
      if(shiftOnto){
        currentStringOnto+=String.fromCharCode(d3.event.keyCode);
      } else {
        currentStringOnto+=String.fromCharCode(d3.event.keyCode-65+97);
      }
      obj1Onto.select('text').text(currentStringOnto);
      updateGraphOnto(node_dataOnto,link_dataOnto);
    }
  }
  if(d3.event.keyCode>=48&&d3.event.keyCode<=57){ //This handles number keys being pressed
    if(editingOnto){
      if(shiftOnto){
         switch(d3.event.keyCode){ //Unfortunately, there was no good way 
           case 48:                //to handle the shifted keys.
             currentStringOnto+=')';
             break;
           case 49:
             currentStringOnto+='!';
             break;
           case 50:
             currentStringOnto+='@';
             break;
           case 51:
             currentStringOnto+='#';
             break;
           case 52:
             currentStringOnto+='$';
             break;
           case 53:
             currentStringOnto+='%';
             break;
           case 54:
             currentStringOnto+='^';
             break;
           case 55:
             currentStringOnto+='&';
             break;
           case 56:
             currentStringOnto+='*';
             break;
           case 57:
             currentStringOnto+='(';
             break;
         }
       } else { //Handling the numbers themselves is much easier.
         currentStringOnto+=(d3.event.keyCode-48).toString();
       }
       obj1Onto.select('text').text(currentStringOnto);
       updateGraphOnto(node_dataOnto,link_dataOnto);
    }
  }
  if(d3.event.keyCode==8){//delete key is pressed
    if(editingOnto){
      d3.event.preventDefault();
      currentStringOnto=currentStringOnto.substring(0,Math.max(currentStringOnto.length-1,0));
      obj1Onto.select('text').text(currentStringOnto);
      updateGraphOnto(node_dataOnto,link_dataOnto);
    } else if (selectedOnto){
      obj1Onto.each(function(d){
          saveEditsOnto();
          removeNodeOnto(d.index);
          selectedOnto=false;
        });
      }
  }
  if(d3.event.keyCode==13){//enter key is pressed
    var node = obj1Onto;
    if(editingOnto){
      saveEditsOnto();
    } else{
      editingOnto=true;
      currentStringOnto=obj1Onto.select('text').text();
      node.select('circle').style('fill','#6f9');
      node.select('text').text(currentStringOnto);
    }
  }
  }
}
//Function to save the current edits that are being done
function saveEditsOnto(){
  var node=obj1Onto;
  if(editingOnto&&node!=null){
   editingOnto=false;
   node.select('text').text(currentStringOnto);
   node.select('circle').style('fill','#69f');
   node.each(function(d){
    d.name=currentStringOnto;
    node_dataOnto[d.index].name = currentStringOnto;
  });
  currentStringOnto="";
  editingOnto=false;
  updateGraphOnto(node_dataOnto,link_dataOnto);
  }
}
//Handler for key up events to toggle the shift value
function onKeyUpOnto(){
  d3.event.preventDefault();
  if(obj1Onto!=null){
    if(d3.event.keyCode==16){
      shiftOnto = false;
    }
  }
}

//Function to have the currentObj point to the currently moused over object (nodes only)
function onMouseoverOnto(){
  currentObjOnto = d3.select(this);
}
function onMouseoutOnto(){
  currentObjOnto = null;
}

//Function that takes an ontology dictionary and resets the graph with the new value
function ontologyToSvgOnto(ontology){
  console.log(ontology);
  var no = [];
  var li = [];
  var keys = Object.keys(ontology);
  for(var i = 0;i<keys.length;i++){ //This is where we 'randomly' place our nodes upon creation.
    var x_pos = 0.2*widthOnto+(i%3)*0.3*widthOnto; //This could serve to be changed.
    var y_pos = 0.2*heightOnto+Math.floor(i/3)*0.3*heightOnto;
    no.push({'name':keys[i],index:i,x:x_pos,y:y_pos});
  }
  node_dataOnto = no;
  for(var i = 0;i<keys.length;i++){
    var ends_list = ontology[keys[i]];
    for(var j = 0;j<ends_list.length;j++){
      var target_index = keys.indexOf(ends_list[j]);
      li.push({source:node_dataOnto[i],target:node_dataOnto[target_index]});
    }
  }
  link_dataOnto = li;
  refreshGraphOnto(node_dataOnto,link_dataOnto);
}

function svgToOntologyOnto(){
  var result = {};
  if(node_dataOnto.length==0) return null;
  for(var i = 0;i<node_dataOnto.length;i++){
    result[node_dataOnto[i].name] = [];
  }
  for(var i = 0;i<link_dataOnto.length;i++){
    result[link_dataOnto[i].source.name].push(link_dataOnto[i].target.name);
  }
  return result;
}

function resizeOnto() {
  var temp_coords = [];
  for(var i = 0; i<node_dataOnto.length;i++){
    temp_coords.push({x:(1.0*node_dataOnto[i].x)/widthOnto,y:(1.0*node_dataOnto[i].y)/heightOnto});
  }
  widthOnto=parseInt(svgOnto.style('width'));
  heightOnto=parseInt(svgOnto.style('height'));
  offsetOnto = 5;
  radiusOnto = widthOnto/25;
  for(var i = 0; i<node_dataOnto.length;i++){
    node_dataOnto[i].x=temp_coords[i].x*widthOnto;
    node_dataOnto[i].y=temp_coords[i].y*heightOnto;
  }
  updateGraphOnto(node_dataOnto,link_dataOnto);
}

d3.select(window).on('resize',resizeOnto);
