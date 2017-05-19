#!/usr/bin/env python3

from functools import partial

def addArgs(argparser, additionalArgs):
    """Adds the additionalArgs to the argparser."""

    # The additonalArgs is a dictionary. The keys of the dictionary
    # are functions names. The values are also a dictionary. The value
    # dictionary's keys are the keywords, the value of the value
    # dictionary is a tuple (default, explation) where default is the
    # keywords default value and explation is the explation.

    for (function, keywordList) in additionalArgs.items():
        # Define the keywords string for the arg parser
        #functionName = '--' + function

        for (keyword, kwargs) in keywordList.items():
            #keywordName = functionName + '-' + keyword
            argName = _buildArgOptName(function, keyword)

            # keywordExplanation = value[1]

            argparser.add_argument(argName, **kwargs)

def applyArgs(userArgs, additionalArgs, absClassLabelers):
    """Applys arguments to the labeler functions."""

    # For each function in the additionalArgs check for the needed
    # additional arguments to apply to the function in
    # absClassLabelers.
    for (functionName, kwargs) in additionalArgs.items():

        # Unpack the arguments from the keywords args kwargs
        newkwargs = {}
        for argName in kwargs.keys():

            argAttrName = _buildArgAttrName(functionName, argName)

            # # Determine if the variable is set in userArgs
            # userArgValue = getattr(userArgs, argAttrName, None)
            # if userArgValue:
            #     # Set the argument parameters
            #     kwargs[argName] = userArgValue
            # else:
            #     # Remove the help string
            #     kwargs[argName] = kwargs[argName][0]

            newkwargs[argName] = getattr(userArgs, argAttrName)
            
            # Wrap the function
            function = absClassLabelers[functionName]
            absClassLabelers[functionName] = partial(function,
                                                     **newkwargs)

######################################################################
#------------------------- internal functions ------------------------
def _buildArgOptName(functionName, keywordName):
    """Builds the argument name to be in the argparser help."""
    return '--' + functionName + '-' + keywordName

def _buildArgAttrName(functionName, keywordName):
    """Builds the argument name to retrieve it from argparser."""
    return functionName + '_' + keywordName
