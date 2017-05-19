#!/usr/bin/env python3

import datetime
import json
import loadPath  # Adds the project path.
import linkograph.labels as llabels
import linkograph.linkoCreate as llinkoCreate
import ontologyExtraction as oe
import os
import sys

def print_usage():

    print("usage:", sys.argv[0], "<JSON commands filename> ...")

def bulk_transform(method):

    for session_filename in sys.argv[1:]:

        #########################
        # create input linkograph
        #########################

        label_rules = open("abstraction.json", "r")
        labeler = llabels.Labeler(json.load(label_rules))
        label_rules.close()
        commands = open(session_filename, "r")
        json_commands = json.load(commands)
        commands.close()
        labeled = labeler.labelCommands(json_commands, "NoLabel")
        llabels.writeLabelsToJsonFile(labeled, "labeled.json")
        ontology_file = open("ontology.json", "r")
        inv_labeling_file = open("labeled.json", "r")
        lg = llinkoCreate.createLinko(json.load(inv_labeling_file), json.load(ontology_file))
        inv_labeling_file.close()
        ontology_file.close()

        ##################################
        # transform linkograph to ontology
        ##################################

        if 0 == method:
            extracted_ontology = oe.simple_lg_to_ontology(lg)
        elif 1 == method:
            extracted_ontology = oe.threshold_lg_to_ontology(lg)
        else:
            print("unknown method:", method)

        #########
        # cleanup
        #########

        os.remove("labeled.json")

if "__main__" == __name__:

    if 2 > len(sys.argv):
        print_usage()
        exit()

    simple_start_datetime = datetime.datetime.now()

    bulk_transform(0)

    simple_end_datetime = datetime.datetime.now()

    bulk_transform(1)

    threshold_end_datetime = datetime.datetime.now()

    simple_run_datetime = simple_end_datetime - simple_start_datetime
    threshold_run_datetime = threshold_end_datetime - simple_end_datetime
    print("simple run time:", simple_run_datetime)
    print("threshold run time:", threshold_run_datetime)
