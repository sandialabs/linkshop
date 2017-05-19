'''
linkServer.py
Author: Jeffrey Bigg, Scott Watson
'''
import thriftpy
import signal
import sys
#Loading in the necessary thrift modules
from thriftpy.protocol import TCyBinaryProtocolFactory
from thriftpy.protocol import TJSONProtocolFactory
from thriftpy.transport import TCyBufferedTransportFactory
from thriftpy.rpc import make_server
import json
import loadPath
import linkograph.linkoCreate as linkoCreate
import linkograph.labels as labels
import linkograph.linkoDrawSVG as linkoDrawSVG
import linkograph.simpleLabels as simpleLabels
import LinkShopSite.models.fileService as fs
import LinkShopSite.stats.statsAggregator as stats
import ontologyExtraction.ontologyExtraction as ont_ext

link_thrift = thriftpy.load("middlewares/thrift/link.thrift", module_name="link_thrift")

#Dispatcher for the implementation of all of the remote procedures as defined in link.thrift
class Dispatcher(object):

  def createLinko(self, commands,ontology,abstraction,linkograph,unique_id):
    """createLinko:
      This function takes the names of the commands, ontology, and abstraction files to be used
      in creating a linkograph, as well as a potential name for the resulting linkograph, and
      returns the name of the saved file. 
    """
    #Come up with a name for the saved linko file
    fileName = commands+ontology+abstraction
    if(len(linkograph)!=0):
      fileName=linkograph
    commandsName = commands

    #Loading in all of the necessary files
    commands = fs.loadFile(commands,'commands',unique_id)['content']
    ontology = fs.loadFile(ontology,'ontology',unique_id)['content']
    abstraction = fs.loadFile(abstraction,'abstraction',unique_id)['content']
    commands = json.loads(commands)
    ontology = json.loads(ontology)
    abstraction = json.loads(abstraction)
    
    #Labeling the commands
    lr = labels.Labeler(abstraction)
    inverseLabeling = lr.labelCommands(commands,defaultLabel="NoLabel")
    inverseLabeling = labels.writesLabelsToJsonFile(inverseLabeling)
 
    #Creating and saving the actual linkograph
    linkograph = linkoCreate.createLinko(inverseLabeling, ontology)
    fileContent = linkoCreate.writesLinkoJson(linkograph)
    fs.saveFile(fileName,fileContent,'linkograph',commandsName,unique_id)
    return fileName


  def drawLinko(self, linkograph, unique_id):
    """drawLinko
      This function takes the file name of a saved linkograph and outputs
      a svg file corresponding to that linkograph.
    """
    linkograph = fs.loadFile(linkograph,'linkograph',unique_id)
    commands = json.loads(fs.loadFile(linkograph['commands'],'commands',unique_id)['content'])
    linkograph = linkoCreate.readsLinkoJson(linkograph['content']) 
    return linkoDrawSVG.linkoDrawSVG(linkograph,commands=commands)


  def saveFile(self, fileName, fileContent,unique_id):
    """saveFile
      This function takes the name of a file to be saved, and the contents
      of that file as a string, and tries to save that file. This is then
      sent off to the file store, which can throw a variety of exceptions,
      all of which are handled here.
    """
    to_send = {
      "res":  "",
      "err":  ""
    }
    try: #A whole lot of things can go wrong here. Beware the user and their input...
      to_send["res"] = fs.saveFile(fileName,fileContent,unique_id=unique_id)
      return json.dumps(to_send)
    except fs.FileNotFound as e:
      to_send["err"] = str(e)
      return json.dumps(to_send)
    except fs.FileTypeNotFound as e:
      to_send["err"] = str(e)
      return json.dumps(to_send)
    except fs.FileTypeMismatch as e:
      to_send["err"] = str(e)
      return json.dumps(to_send)
    else:
      to_send["err"] = "An unexpected error occurred" #Honestly, when are they expected?
      return json.dumps(to_send)


  def fileList(self, fileType,unique_id):
    """fileList
      This function takes a file type and, assuming that file type
      exists, sends out a list of all of the file names that share
      that type, and throws an exception if that file type is not
      found.
    """
    to_send = {
      "list": "",
      "err": ""
    }
    try:
      to_send["list"] = list(fs.fileList(fileType,unique_id))
      return json.dumps(to_send)
    except fs.FileTypeNotFound as e: #Can't send a list that doesn't exist!
      to_send["err"] = str(e)
      return json.dumps(to_send)
    else:
      to_send["err"] = "An unexpected error occurred"
      return json.dumps(to_send)


  def loadFile(self, fileName, fileType,unique_id):
    """loadFile
      This function takes a fileName of type fileType and tries to return
      the contents of that file, assuming that file exists, and throws 
      exceptions when either the file type or file does not exist.
    """
    to_send = {
      'res': "",
      'err': "",
      'data': "",
      'type': fileType
    }
    try:
      to_send['data'] = fs.loadFile(fileName,fileType,unique_id)['content']
      to_send['res'] = fileName +' of type '+fileType+' loaded'
      return json.dumps(to_send)
    except fs.FileTypeNotFound as e:
      to_send['err'] = str(e)
      return json.dumps(to_send)
    except fs.FileNotFound as e:
      to_send['err'] = str(e)
      return json.dumps(to_send)
    else:
      to_send['err'] = 'An unexpected error occurred'
      return json.dumps(to_send)

  def performOntologyRefinement(self, linkograph, ontology, max_changes, unique_id):
    to_send = {
      'err': "",
      'data': {},
    }
    ontology = fs.loadFile(ontology,'ontology',unique_id)['content']
    #print("Here with ontology " + ontology + " and linkograph " + linkograph)
    ontology = json.loads(ontology)
    linkograph = json.loads(linkograph)
    linkoTupleList = []

    for x in range(0, len(linkograph)):
      for label in list(linkograph[x].keys()):
        print("Node " + str(x) + ": " + label + " with links " + str(linkograph[x][label]))
        currLabel = set()
        currLabel.add(label)
        currLinks = set()
        for link in range(0, len(linkograph[x][label])):
          currLinks.add(linkograph[x][label][link])
        linkoTupleList.append((currLabel, set(), currLinks))

    #print("Final list " + str(linkoTupleList))
    linkograph = linkoCreate.Linkograph(linkoTupleList)

    o_prime, accuracy_prime = ont_ext.high_impact_first_minimum_similarity(linkograph, ontology, int(max_changes))

    print("Resulting accuracy " + str(accuracy_prime) + " with ontology " + str(o_prime))

    to_send['data']['o_prime'] = o_prime
    to_send['data']['accuracy_prime'] = accuracy_prime

    return json.dumps(to_send)




  def getStats(self,fileName,startRange,stopRange,unique_id):
    """getStats
      This function will take all of the available statistics on
      a linkograph file (if it exists) in the range of nodes 
      [startRange,stopRange]. 
    """
    to_send = {
      'res':'',
      'err':'',
      'data':''
    }
    try:
      linkograph = fs.loadFile(fileName,'linkograph',unique_id)
      linkograph = linkoCreate.readsLinkoJson(linkograph['content']) 
      to_send['data'] = stats.getStats(linkograph,startRange,stopRange)
      to_send['data'].update({ 'fileName':fileName, 'startRange':startRange, 'stopRange':stopRange })
      return json.dumps(to_send)
    except fs.FileNotFound as e:
      to_send['err'] = str(e)
      return json.dumps(to_send)
    else:
      to_send['err'] = 'An unexpected error occurred'
      return json.dumps(to_send)

#Signal handler to ensure that on a termination signal, the file store saves 
#the state of the system. Probably don't need this anymore.
def signal_handler(signal, frame):
  sys.exit(0) #And now its watch has ended

signal.signal(signal.SIGTERM, signal_handler) #Really, this is just like signing a will

#Starts the thrift service running on port 6000
#Remember, use 127.0.0.1 and not localhost. We still want to avoid the apocalypse!
server = make_server(link_thrift.Link, Dispatcher(), '127.0.0.1', 6000, proto_factory=TCyBinaryProtocolFactory(), trans_factory=TCyBufferedTransportFactory())
print("Service activated")
server.serve()

finished=True
