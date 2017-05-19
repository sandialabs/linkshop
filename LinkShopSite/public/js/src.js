//src.js
//Authors: Jeffrey Bigg + Scott Watson
//Creating a connection back to the server using socket.io
      var socket = io.connect('/', {'sync disconnect on unload': true});

      var shiftPressed = false; // Determines whether the shift key is pressed
      var ctrlPressed = false; // Determines whether the ctrl key is pressed
      var altPressed = false;

      //Upon receiving a message, display the message in the 'output' div
      socket.on("message", function(message){
        console.log("Message from the server arrived");
        message = JSON.parse(message);
        console.log(message);
        if(message.command === 'saveFile'){
          //For this sort of thing, we should expect the following fields:
          //  message.err {only if something wrong happened}
          //  message.res {callback result string}
          //  message.commands {list of command files}
          //  message.ontology {list of ontology files}
          //  message.abstraction {list of abstraction files}
          
          if(message.err.length != 0){
            createAlert(message.err, 'Error:', 'danger', 3);
            return;
          }
          
          if (message.res.length != 0) {
            createAlert(message.res, 'Info:', 'info', 2);
          }

          var abstraction_var = '';
          for (var i = 0; i<message.abstraction.length;i++){
            abstraction_var +='<option value=\''+message.abstraction[i]+'\'>'+message.abstraction[i]+'</option>';
          }
          d3.select('#abstraction').html(abstraction_var);
          var ontology_var = '';
          for (var i = 0; i<message.ontology.length;i++){
            ontology_var +='<option value=\''+message.ontology[i]+'\'>'+message.ontology[i]+'</option>';
          }
          d3.select('#ontology').html(ontology_var);
          var commands_var = '';
          for (var i = 0; i<message.commands.length;i++){
            commands_var+='<option value=\''+message.commands[i]+'\'>'+message.commands[i]+'</option>';
          }
          d3.select('#commands').html(commands_var);
          var linkograph_var = '';
          for (var i = 0; i<message.linkograph.length;i++){
            linkograph_var+='<option value=\''+message.linkograph[i]+'\'>'+message.linkograph[i]+'</option>';
          }
          d3.select('#linkograph').html(linkograph_var);
          loadFile('ontology',$('#ontology').val());
          loadFile('abstraction',$('#abstraction').val());
          drawLinko(); 
        } 
        else if(message.command == 'loadFile') {

          if(message.err.length != 0) {
            createAlert(message.err, 'Error:', 'danger', 3);
            return;
          }

          if (message.type === 'ontology') {
            ontologyToSvgOnto(JSON.parse(message.data));
          }
          if (message.type === 'abstraction'){
            absToSvgAbs(JSON.parse(message.data));
          }
        }
        else if(message.command == 'getStats') {
          if(message.err.length!=0){
            createAlert(message.err, 'Error:', 'danger',3);
            return;
          }
          console.log(message.data);
          statsToSvg(message.data);
        }
        else if (message.command == 'performOntologyRefinement') {
          console.log("Performed ontology refinement with " + message.data);
          var extractedData = JSON.parse(message.data);
          displayOntologyRefinementInformation(extractedData['data']['accuracy_prime'], extractedData['data']['o_prime']);
        }
        else {
          
          if(message.err!=null){
            d3.select('#linkographWorkspace').append("div").attr('id', 'linkographEditor').html(message.err);
            return;
          } 

          linkograph = message.data;
          refreshLinkographs();
        }
      });

      //Upon clicking the Save File button, send the data in the textbox
      //to the server and clear out the textbox
      //Note send_file is asking the server to send a file while
      //  recv_file is asking the server to receive a file
      $(function(){
        $('#saveFile').click(function(){
          var data = {
            command:'saveFile',
            name:$('#fileUp').val(),
            data:'' 
          };
          var file_data = $('#fileUp').prop('files');
          if(file_data.length==0){
            return;
          }
          file_data = file_data[0];
          var reader = new FileReader();
          reader.onload = function(event) {
            data.data = event.target.result;
            if(data.data.length != 0){
              socket.send(JSON.stringify(data));
              $('#fileUp').val('');
            }
          }
          reader.readAsText(file_data);
        });
      });
      $(function(){
        $('#saveAbstraction').click(function(){
          var fileName = prompt('Save file as',$('#abstraction').val());
          var abs = svgToAbstractionAbs();
          if(abs==null) return;
          if(fileName==='') return;
          if(fileName==null) return;
          var fileData = JSON.stringify(abs);
          var data = {
            command:'saveFile',
            name:fileName,
            data:fileData
          };
          socket.send(JSON.stringify(data));
         });
       });
      $(function(){
        $('#saveOntology').click(function(){
          var fileName = prompt('Save file as',$('#ontology').val());
          var onto = svgToOntologyOnto();
          if(onto==null) return;
          if(fileName==='') return;
          if(fileName==null) return;
          var fileData = JSON.stringify(onto);
          var data = {
            command:'saveFile',
            name:fileName,
            data:fileData
          };
          socket.send(JSON.stringify(data));
         });
       });
      //Function to read in file data
      $(function(){
        $('#createLinko').click(function(){
          var commands = $('#commands').val();
          var ontology = $('#ontology').val();
          var abstraction = $('#abstraction').val();
          var linkograph = prompt('Save Linkograph as',commands+ontology+abstraction);
          if(linkograph==null||linkograph==='') return;
          var data = {
            command:'createLinko',
            commands:commands,
            ontology:ontology,
            abstraction:abstraction,
            linkograph:linkograph
          }
          socket.send(JSON.stringify(data));
          $('#linkoName').val('');
        });
      });
      //Function to read in file data
      $(function(){
        $('#performOntologyRefinement').click(function(){
          var ontology = $('#ontology').val();
          var linkograph = JSON.stringify(convertLinkographSVGtoJSON());
          var max_changes_str = prompt("Enter the maximum number of changes for the ontology refinement.", "5");
          var max_changes = parseInt(max_changes_str, 10);
          if(linkograph==null||linkograph===''||isNaN(max_changes_str)||max_changes_str===""){ 
            createAlert("Invalid input.", 'Error:', 'danger',3);
            return;
          }
          var data = {
            command:'performOntologyRefinement',
            ontology:ontology,
            linkograph:linkograph,
            max_changes:max_changes
          }
          socket.send(JSON.stringify(data));
        });
      });

      function performAnalysis(currFile, start, stop){
        var data = {
          command:'getStats',
          fileName:currFile.toString(),
          startRange:parseInt(start),
          stopRange:parseInt(stop)
        };

        socket.send(JSON.stringify(data));
      }

      function drawLinko(){
        var linkograph = $('#linkograph').val();
        var data = {
          command:'drawLinko',
          linkograph:linkograph
        };
        if(linkograph==null || linkograph==='') return;
        socket.send(JSON.stringify(data));
      }
      $(document).ready(function(){
        $('[data-toggle="popover"]').popover();
      });

      function createAlert(message, strong, level, seconds) {
        d3.select('#alertDiv').remove();
        d3.select('#main').append('div').attr('id', 'alertDiv').attr('class', 'alert alert-' + level).html('<strong>' + strong + '</strong> ' + message);
        $('#alertDiv').alert();
        $('#alertDiv').fadeTo(1000 * seconds, 500).slideUp(500, function(){ $("#alertDiv").alert('close'); });
      }

      function loadFile(type, file) {
        var data = {
            command: 'loadFile',
            fileName:file,
            fileType:type
          };
          if(file==null||file==='') return;
          returnedData = socket.send(JSON.stringify(data));
      }

      /**
      keyDown Event Handler
        Catches the keyDown event for user input functionality
      **/
      $(document).keydown(function(event) {
          if(event.which=="16")
              shiftPressed = true;
          else if (event.which=="17")
              ctrlPressed = true;
          else if (event.which=="18")
              altPressed = true;

      });

      /**
      keyUp Event Handler
        Catches the keyUp event to unset variables associated with various user input functions
      **/
      $(document).keyup(function() {
          ctrlPressed = false;
          shiftPressed = false;
          altPressed = false;
      });