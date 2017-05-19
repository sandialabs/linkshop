#!/usr/bin/env python3

import csv
import json
import linkograph.labels as llabels
import linkograph.linkoCreate as llinkoCreate
import linkograph.stats as lstats
import os
import sys
import utils

# a linkograph is a list of tuples (nodes)
# a node is a 3-tuple
# component 0 is a set of labels
# component 1 is a set of backlinks
# component 2 is a set of forelinks

def printNode(node):
    print("labels:", node[0], "backlinks:", node[1], "forelinks:", node[2])

def processSession(session_filename, writer):
    #####################
    # generate linkograph
    #####################

    # label commands
    label_rules = open("abstraction.json", "r")
    labeler = llabels.Labeler(json.load(label_rules))
    label_rules.close()
    commands = open(session_filename, "r")
    json_commands = json.load(commands)
    commands.close()

    if 2 > len(json_commands):
        print("can't process", session_filename, "because session files must have at least two commands")
        return

    last_command = json_commands.pop()

    # access_next, look_next, transfer_next, move_next, execute_next, cleanup_next
    last_command_labels = labeler.labelCommands([last_command], "NoLabel")
    access_next = 0
    look_next = 0
    transfer_next = 0
    move_next = 0
    execute_next = 0
    cleanup_next = 0
    if "Access" in last_command_labels:
        access_next = 1
    if "Look" in last_command_labels:
        look_next = 1
    if "Transfer" in last_command_labels:
        transfer_next = 1
    if "Move" in last_command_labels:
        move_next = 1
    if "Execute" in last_command_labels:
        execute_next = 1
    if "Cleanup" in last_command_labels:
        cleanup_next = 1

    labeled = labeler.labelCommands(json_commands, "NoLabel")

    # @todo cleanup labeled.json when its safe
    llabels.writeLabelsToJsonFile(labeled, "labeled.json")

    # link commands
    ontology = open("ontology.json", "r")
    inv_labeling = open("labeled.json", "r")
    lg = llinkoCreate.createLinko(json.load(inv_labeling), json.load(ontology))
    inv_labeling.close()
    os.remove("labeled.json")
    ontology.close()

    ##################
    # extract features
    ##################

    # node_count
    node_count = len(lg)

    # critical_node_count
    #     @todo: pick something real for critical_threshold
    critical_threshold = node_count / 2
    critical_node_count = lstats.countCriticalNodes(lg, critical_threshold)

    # x_bar, Sigma_x, range_x, y_bar, Sigma_y, range_y
    x_bar, Sigma_x, range_x, y_bar, Sigma_y, range_y = lstats.calculateCartesianStatistics(lg)

    # percentage_of_links
    percentage_of_links = lstats.percentageOfLinks(lg)

    # entropy
    entropy = lstats.graphEntropy(lg)

    # T-Complexity
    encoded_lg = lstats.linkographToString(lg)
    t_complexity = lstats.tComplexity(encoded_lg)

    # link_index
    link_index = lstats.links(lg) / len(lg)

    # graph differences
    graph_differences = lstats.summaryDifference(lg)

    # entropy deviation
    entropy_deviation = lstats.entropyDeviation(lg)

    # mean link coverage
    mean_link_coverage = lstats.meanLinkCoverage(lg)

    # top cover
    top_cover = lstats.topCover(lg)

    first_command = json_commands[0]
    first_datetime = utils.stringToDatetime(first_command['ts'])
    session_start_time = first_datetime.hour * 3600 + first_datetime.minute * 60 + first_datetime.second

    # session_length_seconds, mean_delay_seconds
    last_command = json_commands[-1]
    last_datetime = utils.stringToDatetime(last_command['ts'])
    session_length_timedelta = last_datetime - first_datetime
    session_length_seconds = session_length_timedelta.total_seconds()
    if 1 < len(lg):
        mean_delay_seconds = session_length_seconds / (len(lg) - 1)
    else:
        mean_delay_seconds = None

    # access_ratio, look_ratio, transfer_ratio, move_ratio, execute_ratio, cleanup_ratio
    access_ratio = look_ratio = transfer_ratio = move_ratio = execute_ratio = cleanup_ratio = 0
    if "Access" in labeled.keys():
        access_ratio = len(labeled['Access']) / len(lg)
    if "Look" in labeled.keys():
        look_ratio = len(labeled['Look']) / len(lg)
    if "Transfer" in labeled.keys():
        transfer_ratio = len(labeled['Transfer']) / len(lg)
    if "Move" in labeled.keys():
        move_ratio = len(labeled['Move']) / len(lg)
    if "Execute" in labeled.keys():
        execute_ratio = len(labeled['Execute']) / len(lg)
    if "Cleanup" in labeled.keys():
        cleanup_ratio = len(labeled['Cleanup']) / len(lg)
    
    #################
    # persist in .csv
    #################
    writer.writerow([node_count, critical_node_count, x_bar, Sigma_x, range_x, y_bar, Sigma_y, range_y, percentage_of_links, entropy, t_complexity, link_index, graph_differences, entropy_deviation, mean_link_coverage, top_cover, session_start_time, session_length_seconds, mean_delay_seconds, access_ratio, look_ratio, transfer_ratio, move_ratio, execute_ratio, cleanup_ratio, access_next, look_next, transfer_next, move_next, execute_next, cleanup_next])

def regressionTest():
    # Figure 1 from linkography.pdf
    test_linkograph = llinkoCreate.Linkograph()
    test_linkograph.append((set(), set(), {1, 2, 3}))
    test_linkograph.append((set(), {0}, {2}))
    test_linkograph.append((set(), {0, 1}, set()))
    test_linkograph.append((set(), {0}, set()))
    if (
           4 != lstats.links(test_linkograph)
           or (1.125, 4.5, 1.0, 1.75, 7, 2) != lstats.calculateCartesianStatistics(test_linkograph)
           or 0.0000000000000001 < abs(lstats.percentageOfLinks(test_linkograph) - 0.6666666666666666)
           or 0.0000000000000001 < abs(lstats.graphEntropy(test_linkograph) - 0.9182958340544896)
       ):
        print("error calculating statistics for training data")

def printUsage():
    print("usage: python3 extractSessionFeatures.py <JSON commands filename> ...")

def main(args):
    regressionTest()

    if 1 > len(args):
        printUsage()
        exit()

    # open CSV and write column headers
    csv_file = open("session_features.csv", "w", newline="")
    writer = csv.writer(csv_file)
    writer.writerow(["node_count", "critical_node_count", "x_bar", "Sigma_x", "range_x", "y_bar", "Sigma_y", "range_y", "percentage_of_links", "entropy", "t_complexity", "link_index", "graph_differences", "entropy_deviation", "mean_link_coverage", "top_cover", "session_start_time", "session_length_seconds", "mean_delay_seconds", "access_ratio", "look_ratio", "transfer_ratio", "move_ratio", "execute_ratio", "cleanup_ratio", "access_next", "look_next", "transfer_next", "move_next", "execute_next", "cleanup_next"])

    # extract features from each session
    for session_filename in args:
        processSession(session_filename, writer)

    # close CSV
    csv_file.close()

if "__main__" == __name__:
    main(sys.argv[1:])
