#!/usr/bin/env python3

""" Methods for manipulating json files into individual sessions."""

import json  # For handling files in the json format
import argparse  # For command line parsing
import sys # For argv
import datetime # For parsing dates and times
import shutil # For deleting directries
import os # For creating directories
import errno #Capturing file system errors

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def readJson(file, time, outDir):
    """ Read a Linkograph from a json file. """
    with open(file, 'r') as inputFile:
        jsonFile = json.load(inputFile)
        date_format_string = "%m/%d/%Y %I:%M:%S %p"
        currentDate = None
        prevDate = None
        sessionNumber = 1
        baseOutputName= outDir + "/session"
        sessionList = []
        diff = datetime.timedelta(seconds=1)

        for entry in jsonFile:
            if currentDate == None:
                currentDate = datetime.datetime.strptime(entry["ts"], date_format_string)
            else: 
                prevDate = currentDate
                currentDate = datetime.datetime.strptime(entry["ts"], date_format_string)
                diff = (currentDate-prevDate)

            if diff.seconds > time:
                print("Found a new session " + str(diff.seconds))
                outputFileName = baseOutputName + '%d.json' % sessionNumber
                with open(outputFileName, 'w') as outputFile:
                    json.dump(sessionList, outputFile, indent=4)
                sessionNumber += 1
                sessionList = []
                sessionList.append(entry)
            else:
#                print(diff)
                sessionList.append(entry)

        if len(sessionList) > 0:
            outputFileName = baseOutputName + '%d.json' % sessionNumber
            with open(outputFileName, 'w') as outputFile:
                json.dump(sessionList, outputFile, indent=4)
        print("Found " + str(sessionNumber) + " sessions")


######################################################################
#----------------------- Command Line Programs -----------------------


def cli_sessionize(argv=None):
    """Separates a command data file into sessions."""

    info = 'Sessionize a json file into sessions that are seperated by an hour or more.'

    parser = argparse.ArgumentParser(description=info)

    parser.add_argument('-i', '--input', metavar='INPUT_FILE', required=True,
                        help='the json to sessionize')

    parser.add_argument('-o', '--output', metavar='OUPUT_DIR', required=True,
                        help='directory to place results')

    parser.add_argument('-t', '--time', metavar='TIME', type=int,
                        help='time between sessions in seconds')

    args = parser.parse_args()

    infile = None
    if args.input:
        infile = args.input

    outDir = None
    if args.output:
        outDir = args.output
        shutil.rmtree(outDir, ignore_errors=True)
        make_sure_path_exists(outDir)

    time = 3600
    if args.time:
        time = args.time


    readJson(infile, time, outDir)

if __name__ == '__main__':
    cli_sessionize(sys.argv)
