#~/usr/bin/env python3


import argparse  # For parsing command line arguments.
import json  # For reading the json format.
import re  # For pattern matching.

def labelCommands(commands, labelRules, defaultLabel = None):
    """Labels the commands according to the label rules.

    Label rules are of the form (cmd pattern, arg pattern). Rules can
    be combined such as
    (cmd pattern, arg pattern)&(cmd patter, arg pattern) 
    When rules are combined, they represent a label that represents a
    sequence of commands. For example, ('dir', '.*')&('ping', '.*')
    matches the sequence of commands
        dir
        ping
    but does not match
        dir
        ifconfig
        ping.

    Note: multiple command rules has not been implemented yet.

    The labels are returned a dictionary with keys the labels and
    values the set of lines with the corresponding labels.
    """

    labels = {}

    if not len(commands) or not len(labelRules):
        return labels

    labels = {key: [] for key in  labelRules.keys()}

    # Loop through every command.
    lineNum = 0 # Keeps track of the current line.
    for line in commands:
        # The command is packed in a dictionary.
        cmdSplit = line['cmd'].split(None, 1)
        cmd = cmdSplit[0]
        arg = ''
        if len(cmdSplit) > 1:
            arg = cmdSplit[1]

        # Check against the rules.
        matched = False
        for currentLabel in labelRules:
            # Command pattern and argument pattern.
            patterns = labelRules[currentLabel]
            cmdPattern = patterns[0]
            argPattern = patterns[1]
            
            if (re.match(cmdPattern, cmd, re.IGNORECASE) and
                re.match(argPattern, arg)):
                labels[currentLabel].append(lineNum)
                matched |= True

        if defaultLabel and not matched:
            default = labels.get(defaultLabel)
            if not default:
                labels[defaultLabel] = [lineNum]
            else:
                default.append(lineNum)

        lineNum += 1

    return labels

######################################################################
#----------------------- Command Line Programs -----------------------

def cli_labelCommands():
    """Command-line interface for labeling commands.


    Uses the simpleLabels functions for labeling commands.

    """


    info = 'Uses the simpleLabels scheme for labeling commands.'

    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('commandFile', metavar='COMMANDS.json',
                         nargs=1,
                         help='the json of commands to label')
    parser.add_argument('labelRulesFile', metavar='LABELS.json',
                        nargs=1,
                        help='the json of labeling rules.')
    parser.add_argument('-o', '--out', metavar='OUTPUT_FILE',
                        help='file for writing the label object.')

    args = parser.parse_args()

    # Read in the commands from the json file.
    commands = json.load(open(args.commandFile[0], 'r'))

    # Read in the rules.
    rules = json.load(open(args.labelRulesFile[0], 'r'))

    labels = labelCommands(commands, rules, 'NoLabel')

    if args.out:
        outfile = open(args.out, 'w')
        json.dump(labels, outfile, indent=4)
    else:
        print(json.dumps(labels, indent=4))

if __name__ == '__main__':
    cli_labelCommands()
