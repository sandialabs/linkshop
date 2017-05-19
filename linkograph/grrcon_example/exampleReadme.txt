This file describes one example of running the commands in labels.py,
linkoCreate.py, and linkoDraw.py to go from encrypted input commands to a
pictorial representation of a linkograph.

Files that you will need: labels.py, linkoCreate.py, linkoDraw.py,
linkoSVG.py, anon.py, util.py, p2.txt, english.txt, SLMC.json,
SLMC_SelfLinks.json, and grrcon-encoded.json.

As of the creation of this file, labels.py, linkoCreate.py,
linkoDraw.py, and linkoSVG.py are in the linkograph folder. The
anon.py script, util.py, p2.txt and english.txt are in the python
folder (which will probably be change to anon or anonymize in the
future). The json files SLMC.json and SLMC_SelfLinko.json are in the
linkograph/grrcon_example folder and grrcon-encoded.json is in the
files folder.

In the following, commands that are ran in from the command line start
with '$' and commands ran in the python3 interpreter start with
'>>>'. Of course, the commands ran in the interpreter can be wrapped
to run from the command line.

The first things is to decrypt the grrcon_commands and strip the
output. The command

$ ./anon.py -k "DCcOIqE9gfAMq2Qn0t3Dfy7YDDkIRDyz0y8n5/IHDRc=" -j -s \
grrcon-encoded.json > grrcon_commands.json

The script anon.py is the anonymization script. The option -k provides
the key, -j indicates we are reading a json file and not an ordinary
file, -s strips the output. Finally, anon prints to the consoles, so
we are redirecting the result into the file grrcon_commands.json. Thus
grrcon_commands.json is our anonymized grrcon commands json file.

The next step is to provide labels. The lables.py package has the
function labelCommands which handles labeling the commands. We are
going to do the following labeling. The commands ipconfig, net, ping,
and dir are going to be labeled 'LookAround'. The 'command' download
present in the grrcon data will be labeled 'Downloading'. The command
cd will be labeled 'Move'. The command del will be labeled
'Cleanup'. Any command followed by exe will be labeled
'Commands'. Finally, the command cmd.exe will be labeled 'Shell'. To
accomplish this, we use the SLMC.json file. This file is a dictionary
for the form {label:[ command_pattern, argument_pattern]}. Both the
patterns command_pattern and argument_pattern are python3 regular
expressions and are matched against the command and argument,
respectively. For example, if given a command 'cmd arg', the
command_pattern is matched against 'cmd' and argument_pattern is
matched against 'arg'. If both patterns match, then the line is given
the corresponding label. Note: lines can have more than one label. For
this initial version, it is assumed that the command is the first word
of the string when split on whitespace. As a concrete example,
SLMC.json contains the entry:
    "LookAround": ["ipconfig|ping|dir|net", ".*']
Thus a LookAround will match:
     ipconfig
     net view
     pint -n name
     dir

The command labelCommands from the labels.py package handles applying
the labels from a label json file to the commands provided by a
command json file. The following sequence of commands will apply the
labels of SLMC.json to the commands in grrcon_commands.json and will
write the results to SLMCLabeled.json.

>>> import labels

>>> labels.labelCommands('grrcon_commands.json','SLMC.json',
    'SLMCLabeled.json', 'NoLabel')

It is possible, that some commands do not match any expressions for
the labels. Passing 'NoLabel' gives these unmatched commands the label
'NoLabel'. The SLMCLabel.json file is a dictionary {label:[line,
line,..., line]} that maps label to a list of line numbers. For
example, SLMCLabeled.json contains the entry "Move":[5,7] which means
lines 5 and 7 (zero indexed) are labeled Move.

Next, we will create a linkograph from a set of rules. A rules json
contains essentially a graph. The form is a dictionary
{initialLabel:[targetLabel, targetLabel, ..., targetLabel]}. This
indicates a directed line from initialLabel to each of the
targetLabels, that is
    initialLabel -> targetLabel
Given a directed line intialLabel -> targetLabel, the createLinko
function of the linkoCreate package will create a forelink from any line
labeled initialLabel to all lines following labeld targetLabel. For
this example, we will use the trivial rule json file
SLMC_SelfLinks.json which maps all the labels to themselves except the
NoLabel, which is ignored. Self labels create a linkograph where all
all commands that have the same label are connected. Thus dense
connections illustrate places wich a high activity for the given
label. The following command creates a linkograph using the labels
SLMCLabeled.json and rules SLMC_SelfLinks.json.

>>> import linkoCreate

>>> linko = linkoCreate.createLinko('SLMCLabeled.json',
    'SLMC_SelfLinks.json')

What is returned by this command is a Linkograph data structure which
is a class that extends a list so that attributes can be
added. Currently, the only default attribute is a list of the
labels. The entries of the Linkograph list are tuples consisting of
three sets: labels, backlinks, forelinks. Thus a two node linkograph
with a single link could look like:
  l = [({'F'}, {}, {1}), ({'Be'}, {0}, {})]
Here the first item is labeled 'F' and the scond item is labeled
'Be'. The 1 indicates that there is a forelink to Be node and the 0
indicates there is a backlink to the F node. This linkograph would
also have the attribute
  l.labels = ['F', 'Be']

A linkograph can also be written to a json by using the function:


>>> linkoCreate.writeLinkoJson(linko, 'Linko_SLMCLabels_SLMC_SelfLinks.json')

This command takes the linkograph linko and writes it to the json file
Linko_SLMCLabels_SLMC_SelfLinkos.json. The linkograph cannot be
directly dump to a json using the json.dump since sets are not
supported. The writeLinkoJson creates a structure that can be passed
to the json.dump by creating an array where the first entry is the
labels array attribute and the following entries are the linkograph
tuples converted to an array of arrays, that is the tuple and the sets
are changed to arrays.

Given the linkograph list, there are two functions for creating
pictorial representations: one creates a postscript file and the other
creates an SVG embedded in html. The following command creates the PS.

>>> import linkoDraw

>>> linkoDraw.linkoDrawEPS(linko, 'Linko_SLMCLabels_SLMC_SelfLinko.ps')

The html file can be created by running:

>>> import linkoSVG

>>> linkoSVG.linkoDrawSVG(linko, 'Linko_SLMCLabels_SLMC_SelfLinko.html')
