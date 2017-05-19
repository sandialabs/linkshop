#!/user/bin/env python3

# For this demo, we will use the ontology.json and its abstraction
# classes.

import json # For manipulting json files

# Read in the ontology
ontFile = open('resources/ontology.json', 'r')
ont = json.load(ontFile)
ontFile.close()

# Get the abstraction classes
absClasses = list(ont.keys())
absClasses.sort()

# Now we will get the Markov model functions
import markov.Model as markel # For Markov model functions

# We will generate a Markov model with six states based
# off the absraction classes in absClasses
model = markel.genModel(6, absClasses=absClasses, ontology=ont,
                        seed=42)

# The abstraction classes
model.absClasses

# The ontology
model.ontology

# The transition matrix
model.tMatrix

# The current state
model.current()

# Create a dot representation
dotString = model.toDot()

# The dot file can be create by writing this string to a file.
dotFile = open('resources/model.dot', 'w')
dotFile.write(dotString)
dotFile.close()

# The current state of the model can be save by recording the current
# state or by using the state attibute
currentAbsClass = model.current()
currentState = model.state

# The next member function advances the markov model forward one state
model.next()

# The genLinkograph function creates a linkograph of a given size
linko8 = model.genLinkograph(8)

# A fun way to see the linkograph is to use the ASCII printer
import linkograph.linkoDrawASCII as llda # For ASCII printing
llda.linkoPrint(linko8)

# We can save our Markov model using the json interface
markel.writeJson(model, 'resources/model.json')

# We can also read in the Markov model
model2 = markel.readJson('resources/model.json')

# We can use the distance function to verify that the transition
# matrices are the same. Note that this does not in itself show that
# the Markov models are the same since there is a lot more state than
# this.
model.dist(model2)

# We can also create a Markov model based on an ontology
modelOnt = markel.genModelFromOntology(ont, seed=42)
modelOnt.tMatrix

# We can also create Markov models based on linkographs
# First we create a linkograph of size 100
linko100 = model.genLinkograph(100)
linko100.labels

# Now we create a Markov model using the 'link' method which creates a
# Markov model such that he probability of the transition 'A' to 'B'
# is the same as the percentage of links that have a terminal node
# labeled 'B', provided the current node is labeled 'A'.
modelLinkoLink = markel.genModelFromLinko(linko100, ontology=ont,
                                          seed=42, method='link')

# Now we create a Markov model useing the 'next method wich creae a
# Markove mode such that the probability for the transition 'A' to 'B'
# represents is the percentage of time the next node was labeled 'B'
# provided the current node is 'A'.
modelLinkoNext = markel.genModelFromLinko(linko100, ontology=ont,
                                          seed=42, method='next')
