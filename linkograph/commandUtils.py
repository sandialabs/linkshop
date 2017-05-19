#!/usr/bin/env python3

"""Methods for processing files associated with linkographs."""

import json  # For processing json files.
import argparse  # for the cli.

def selectCommands(commands, indexList, lineNumbers=False):
    """Prints commands indexed by the list passed."""

    commandList = []

    for index in indexList:
        record = commands[index]['cmd']

        if lineNumbers:
            record = (index, record)

        commandList.append(record)

    return commandList


######################################################################
#----------------------- Command Line Programs -----------------------

def cli_selectCommands():
    """Cli for selectCommands"""

    info = 'Creates a json file for the subset of commands passed.'

    parser = argparse.ArgumentParser(description=info)

    parser.add_argument('commands', metavar='COMMANDS.json',
                        nargs=1,
                        help='the command json file.')

    parser.add_argument('indexList', metavar='INDEX_LIST.json',
                        nargs=1,
                        help='the index list json file.')

    parser.add_argument('-o', '--output', 
                        help='the output json file.')

    parser.add_argument('-l', '--lineNumbers',
                        action='store_true',
                        help='print line numbers.')

    args = parser.parse_args()

    with open(args.commands[0], 'r') as commandsFh:
        commands = json.load(commandsFh)
        
    with open(args.indexList[0], 'r') as indexListFh:
        indexList = json.load(indexListFh)

    output = selectCommands(commands, indexList, args.lineNumbers)

    if args.output is not None:
        with open(output.json, 'w') as outputFh:
            json.dump(output, outputFh, indent=4)

    else:
        print(json.dumps(output, indent=4))
