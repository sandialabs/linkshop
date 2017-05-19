import json
import os
import pymongo

'''
fileService.py
Author: Jeffrey Bigg
'''



mongo_client = pymongo.MongoClient() 
#db = {}
'''
initialize

Takes a 'unique_id'entifier and sets up a database in MongoDB 
and ensures that that database has collections associated with
the various file types that are stored.
'''
def initialize(unique_id='default'):
    #global db
    #if unique_id is None:
    #    unique_id = 'default';
    db = mongo_client[unique_id]
    if(not 'ontology' in db.collection_names()):
        db.create_collection('ontology')
    if(not 'abstraction' in db.collection_names()):
        db.create_collection('abstraction')
    if(not 'commands' in db.collection_names()):
        db.create_collection('commands')
    if(not 'linkograph' in db.collection_names()):
        db.create_collection('linkograph')
    return db

'''
FileNotFound

Custom exception class for reporting a file not found exception.
Value should be the name of the file as a string.
'''
class FileNotFound(Exception):
    def __init__(self, value):
        self.value=value
    def __str__(self):
        return "File "+self.value+" not found!"

'''
FileTypeNotFound

Custom exception class for reporting a file type not found.
Value should be the name of the file type as a string.
'''
class FileTypeNotFound(Exception):
    def __init__(self,value):
        self.value=value
    def __str__(self):
        return "File type "+self.value+" not found!"

'''
FileTypeMismatch

Custom exception class for reporting a conflict in a type given
by the user and a type found by the type detection system.
Given and found should both be the file types as strings.
'''
class FileTypeMismatch(Exception):
    def __init__(self,given,found):
        self.given = given
        self.found = found
    def __str__(self):
        return "Given "+self.given+", but found "+self.found

'''
loadFile

Looks for a fileName of fileType. Both arguments are strings.
Upon success returns the file, throws exceptions when either
the type or name is not found.
'''
def loadFile(fileName,fileType,unique_id='default'):
    db=initialize(unique_id)
    if (not fileType in db.collection_names()):
        raise FileTypeNotFound(fileType)
    if (None==db[fileType].find_one({'name':fileName})):
        raise FileNotFound(fileName)
    result = db[fileType].find_one({'name':fileName})
    result.pop('_id',None) #Removes the MongoDB object id
    return result #What will usually be returned is a dictionary
                  #of the type {'name':[...],'content':[....]}.
                  #The caller will be responsible for handling
                  #this format.
'''
fileList

Returns a list of all of the file names for files of
type fileType. Argument is a string. Throws error when
fileType is not found.
'''
def fileList(fileType,unique_id='default'):
    db=initialize(unique_id)
    if (not fileType in db.collection_names()):
        raise FileTypeNotFound(fileType)
    results = []
    for record in db[fileType].find():
        if 'name' in record:
            results.append(record['name']) 
    return results

'''
saveLinko

Helper function for saving a linkograph.
All arguments are strings. Throws an error if the commandsName
file cannot be found.
'''
def saveLinko(fileName,fileContent,commandsName,unique_id):
    try:
        db=initialize(unique_id)
        loadFile(commandsName,'commands',unique_id)
        toSave = {}
        toSave['content'] = fileContent
        toSave['commands'] = commandsName
        toSave['name']=fileName
        db['linkograph'].insert_one(toSave)
        return "File " +fileName + " is saved as type linkograph"
    except:
        raise FileNotFound(fileName)
    
'''
saveFile

Takes a file and the content stored in it and saves it in the file store.
If the fileType is unknown or there is a mismatch, and exception is thrown.
If fileType isn't given, the system will try and detect the file type.
Stores it in the mongo database in the format of {'name':fileName,'content':
fileContent}, except in the case of a linkograph, at which point it the commandsName is stored along with it with a key of 'commands'.
'''
def saveFile(fileName,fileContent,fileType=None,commandsName=None,unique_id='default'):
    db=initialize(unique_id)
    if fileType==None:
        fileType=detectFiletype(fileContent)
    else:
        if not fileType == detectFiletype(fileContent):
            raise FileTypeMismatch(fileType,detectFiletype(fileContent))
    if fileType == "Unknown file":
        raise FileTypeNotFound(fileType)        
    if fileType == "linkograph":
        if commandsName==None:
            raise FileNotFound("commands file")
        return saveLinko(fileName,fileContent,commandsName,unique_id)
    if fileType in db.collection_names():
        if not None==db[fileType].find_one({'name':fileName}):
            if fileContent==db[fileType].find_one({'name':fileName})['content']:
                return "We already have "+fileName
            else:
                fileName=fileName+"new"
                return saveFile(fileName,fileContent,fileType,unique_id=unique_id)
        else:
            toSave = {}
            toSave['name'] = fileName
            toSave['content'] = fileContent
            db[fileType].insert_one(toSave)
            return "File "+fileName+" saved as type "+fileType
    raise FileTypeNotFound(fileType)
                
'''
detectFiletype

Function which takes the contents of a file and tries to detect what sort
of file it is. Currently has support for detecting commands, abstraction
and ontology files.
'''
def detectFiletype(fileContent):
    try:
        file_parsed = json.loads(fileContent)
        if (type(file_parsed) is list):
            if(type(file_parsed[0]) is dict):
                if("ts" in file_parsed[0] and "cmd" in file_parsed[0]):
                    return "commands"
                else:
                    return "Unknown file"
            if(type(file_parsed[0]) is list):
                if(len(file_parsed[0])==0):
                    return "Unknown file"
                for label in file_parsed[0]:
                    if not type(label) is str:
                        return "Unknown file"
                for tupl in file_parsed[1:]:
                    if not type(tupl) is list:
                        return "Unknown file"
                    if not len(tupl)==3:
                        return "Unknown file"
                return "linkograph"
            return "Unknown file"
        elif (type(file_parsed) is dict):
            if(len(file_parsed.keys())==0):
                return "Unknown file"
            longest_entry = []
            for key in file_parsed:
                if not type(file_parsed[key]) is list:
                    return "Unknown file"
                if len(file_parsed[key])>len(longest_entry):
                    longest_entry=file_parsed[key]
            if len(longest_entry)==0:
                return "Unknown file"
            if type(longest_entry[0]) is str:
                return "ontology"
            if type(longest_entry[0]) is dict:
                if "command" in longest_entry[0]:
                    return "abstraction"
            return "Unknown file"
        return "Unknown file"
    except:
        return "Unknown file"

#initialize() 
