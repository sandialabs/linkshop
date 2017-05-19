//See? Libraries are important!
var express = require('../middlewares/node_modules/express');
var http = require('http');
var io = require('../middlewares/node_modules/socket.io');
var net = require('net');
var thrift = require('../middlewares/node_modules/thrift');
var link_svc = require('../middlewares/thrift/gen-nodejs/Link.js');
var ttypes = require('../middlewares/thrift/gen-nodejs/link_types.js');
var assert = require('assert');
var transport = thrift.TBufferedTransport()
var protocol = thrift.TBinaryProtocol()

//fileClient.js
//Author: Jeffrey Bigg

//Load in express server handler
var app = express();
app.use(express.static('./public'));//I hope the user doesn't realize
                                    //they can access the source javascript
                                    //or, heavens forbid, the css file!

//Create the actual server listening on port 9090
var server = http.createServer(app).listen(9090);
console.log('Server started on port 9090');//Like port 8080, but higher!

//Create a socket listener
var io = io.listen(server);

//Fix to allow for library includes on the front end
//Note: This requires socket.io to be before version 1.0
//If you get a CORS error, try the following command:
//    sudo npm install --save socket.io@"<1.0"
io.set('origins','*:*');
//Believe me, it's a pain you don't want to have to go through

io.set('transports',['xhr-polling']);

//Connection handler
io.sockets.on('connection', function(socket){
  console.log('Connection with server established');//Such wonderful unauthenticated goodness.
                                                    //We really need to fix that at some point.

  //First create a connection to the thrift python server
  //Connections to the thrift python server should be on a 
  //  per connection basis.
  var connection = thrift.createConnection('127.0.0.1', 6000, { //Use 127.0.0.1, and NOT localhost.
      transport : transport,                                    //Using localhost causes this to not
      protocol : protocol                                       //work, and brings us that much closer
  });                                                           //to the apocalypse.

  var unique_id = 'defaulted'; //This will be useful later
  
  connection.on('error', function(err) {
    console.log(err); //In case we screw up. Which happens.
  });

  //Create the client for this connection to use
  var client = thrift.createClient(link_svc, connection);

  /**
  sendError
    This function is a standard method for sending an error
    back to the frontend client.
  **/
  function sendError(command,err,sock){
    var message_to_client = {
      command: command,
      err: err
    };
    sock.send(JSON.stringify(message_to_client)); //I hope the client is
                                                  //ready for the bad news
  }
  /**
  sendLists
    This function gets the lists of all of the file names of the
    different kinds of files and sends them over to the client.
  **/
  function sendLists(client,socket){
    client.fileList('commands',unique_id, function(err, response){
      client.fileList('ontology',unique_id, function(err1, response1){
        client.fileList('abstraction',unique_id, function(err2,response2){
          client.fileList('linkograph',unique_id, function(err3,response3){
            //So much nesting you would think a bald eagle lived here.
            //Or one of those weird Russian dolls.
            message = JSON.parse(response);
            message1 = JSON.parse(response1);
            message2 = JSON.parse(response2);
            message3 = JSON.parse(response3);
            if(message.err.length!=0){
              sendError('saveFile',message.err,socket);
              return;
            }
            if(message1.err.length!=0){
              sendError('saveFile',message1.err,socket);
              return;
            }
            if(message2.err.length!=0){
              sendError('saveFile',message2.err,socket);
              return;
            }
            if(message3.err.length!=0){
              sendError('saveFile',message3.err,socket);
              return;
            } //Gotta love that error handling.
            command = 'saveFile'
            err = '';
            res = '';
            message_to_client = {
              command: command,
              err: err,
              res: res,
              commands: message.list,
              ontology: message1.list,
              abstraction: message2.list,
              linkograph: message3.list
            };
            socket.send(JSON.stringify(message_to_client));
          });
        });
      });
    });
  }

  //Start off the connection by making sure that the client has 
  //the most up-to-date file name lists
  sendLists(client,socket);

  //Socket message handler
  socket.on('message', function(data){
    
    //Collect the data and find the command
    data = JSON.parse(data);
    command = data.command;
    console.log(command+' command received');

    if (command === 'createLinko') { //Handles a request to make a linkograph

      ontology = data.ontology;
      abstraction = data.abstraction;
      commands = data.commands;
      linkograph = data.linkograph;
      if(linkograph==null){
        linkograph="";
      }
      if(ontology==null || abstraction==null || commands==null || ontology==='' || abstraction==='' || commands===''){
        sendError('createLinko','Files missing!',socket); //Checking for null and empty string because with some browsers
        return;                                           //no selection is a null, and with others it's an empty string.
      }
      client.createLinko(commands,ontology,abstraction,linkograph,unique_id, function(err,response){
        //No error handling! Again! I really must fix this.
        linkograph = response
        client.drawLinko(linkograph,unique_id, function(err,response){  
          var message_to_client = {
            command: 'createLinko',
            data: response
          };
          socket.send(JSON.stringify(message_to_client));
        });
      });
      sendLists(client,socket);
    } else if (command ==='saveFile') { //Handles a request to save some raw input file
      fileName = data.name;
      fileContent = data.data;
      client.saveFile(fileName,fileContent,unique_id, function(err, response){
        //Expecting a response in the form of:
        //  message.err
        //  message.res
        message = JSON.parse(response);
        if(message.err.length!=0){
          sendError('saveFile',message.err,socket);
          return;
        }
        sendLists(client,socket);
      });
    } else if (command === 'loadFile'){ //Handles a request for file content
      fileName = data.fileName;
      fileType = data.fileType;
      client.loadFile(fileName,fileType,unique_id,function(err,response){
        res_data = JSON.parse(response);
        if(res_data.err.length!=0){ //Error handling! Yes! 
          sendError('loadFile',res_data.err,socket);
//                     ^ 
//Mmmm look at that   /|\ That's to prevent a race condition
//hard coded goodness! |  where the command variable was reused
//_____________________|  before a handler was finished... handling.
          return;
        }
        var message_to_client = {
          command: 'loadFile',
          err: res_data.err,
          res: res_data.res,
          data: res_data.data,
          type: res_data.type
        }
        socket.send(JSON.stringify(message_to_client));
      });
    } else if (command === 'drawLinko'){ //Handles a request for a SVG linkograph
      linkograph = data.linkograph;
      if(linkograph==null||linkograph===''){//Can't ask for something that doesn't
                                            //exist yet. If you can, it's probably
                                            //a race condition and that's not kosher
        sendError('drawLinko',"Files missing!",socket);
        return;
      }
      client.drawLinko(linkograph,unique_id,function(err,response){//We're being far too trusting here
                                                         //and that should be fixed
        var message_to_client = {
          command: 'drawLinko',
          data: response
        };
        socket.send(JSON.stringify(message_to_client));
      });
    } else if (command === 'performOntologyRefinement'){ //Handles a request for a SVG linkograph
      linkograph = data.linkograph;
      ontology = data.ontology;
      max_changes = data.max_changes;
      if(linkograph==null||linkograph===''||ontology==null||ontology===''){//Can't ask for something that doesn't
                                            //exist yet. If you can, it's probably
                                            //a race condition and that's not kosher
        sendError('performOntologyRefinement',"Files missing!",socket);
        return;
      }
      client.performOntologyRefinement(linkograph,ontology,max_changes,unique_id,function(err,response){//We're being far too trusting here
                                                         //and that should be fixed
        var message_to_client = {
          command: 'performOntologyRefinement',
          data: response
        };
        socket.send(JSON.stringify(message_to_client));
      });
    } else if (command === 'getStats'){ //Handles a request for statistics on a linkograph
      fileName = data.fileName; //This should be the name of a linkograph file
      startRange = data.startRange; //These range values should be integers
      stopRange = data.stopRange;
      if(fileName==null||fileName===''){ //Input sanitation
        sendError('getStats','File missing!',socket);
        return;
      }
      if(startRange==null||stopRange==null||!(typeof startRange == 'number')||!(typeof stopRange == 'number')){ //Some input sanitation
        sendError('getStats','Invalid range!',socket);
        return;
      }  
      if(startRange>stopRange){ //If we let this happen, we wouldn't be very good people
        sendError('getStats','Invalid range!',socket);
        return;
      }
      client.getStats(fileName,startRange,stopRange,unique_id,function(err,response){
        res_data = JSON.parse(response);
        if(res_data.err.length!=0){ //If something terrible happened, let the client know 
                                    //(not always the best policy, but it works here)
          sendError('getStats',res_data.err,socket);
          return;
        }
        message_to_client = {
          command: 'getStats',
          err: res_data.err,
          res: res_data.res,
          data: res_data.data
        };
        //Send those statistics. Clients love statistics.
        socket.send(JSON.stringify(message_to_client));
      });
    } else {
      //If you've got no idea what you're told to do, throw your hands up in the air...
      console.log('Error: Command \''+command+'\' unknown');
      //...and send an update just in case!
      sendLists(client,socket);
    }
    });

  //Make sure to clean up upon disconnect
  socket.on("disconnect", function() {
    console.log("Connection ended"); //We're very tidy people
    connection.end();
  });
}); 

var chaos = true;
