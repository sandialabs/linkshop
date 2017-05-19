#!/usr/bin/env python3

import os

import calculateFirstClusterPredictors
import campaignAnalysis
import extractCommandFeatures
import extractSessionFeatures
import synthesizeSessions
import transformClustersToAbstraction

if "__main__" == __name__:

    # synthesizeSessions.py transforms many command JSONs into many more command JSONs
    # e.g., grrcon_commands.json.2, grrcon_commands.json.3, ...
    synthesizeSessions.main(["grrcon_commands.json"])
    for i in range(2, 23):
        outfilename = "grrcon_commands.json." + str(i)
        if not os.path.isfile(outfilename):
            print("synthesizeSessions unit test failed")
            exit()

    # extractSessionFeatures.py extracts session features from many command JSONs and outputs into a CSV
    # e.g., session_features.csv
    extractSessionFeatures.main(["grrcon_commands.json.2", "grrcon_commands.json.3"])
    if not os.path.isfile("session_features.csv"):
        print("extractSessionFeatures unit test failed")
        exit()

    # extractCommandFeatures.py extracts command features from many command JSONs and outputs into a command features CSV
    # e.g., command_features.csv
    extractCommandFeatures.main(["grrcon_commands.json.2", "grrcon_commands.json.3"])
    if not os.path.isfile("command_features.csv"):
        print("extractCommandFeatures unit test failed")
        exit()

    # campaignAnalysis.py transforms many command JSONs into a CSV suitable for analysis of the entire campaign
    # e.g., campaign_analysis.csv
    campaignAnalysis.main(["grrcon_commands.json.2", "grrcon_commands.json.3"])
    if not os.path.isfile("campaign_analysis.csv"):
        print("campaignAnalysis unit test failed")
        exit()

    # calculateFirstClusterPredictors.py transforms a command features CSV
    # e.g., cluster_features.csv
    calculateFirstClusterPredictors.main(["command_features.csv"])
    if not os.path.isfile("cluster_features.csv"):
        print("calculateFirstClusterPredictors unit test failed")
        exit()

    # transformClustersToAbstraction.py transforms a clusters CSV into an abstraction JSON
    # e.g., cluster_features.csv.json
    transformClustersToAbstraction.main(["cluster_features.csv"])
    if not os.path.isfile("cluster_features.csv.json"):
        print("transformClustersToAbstraction unit test failed")
        exit()

    # clean up results from test
    for i in range(2, 23):
        os.remove("grrcon_commands.json." + str(i))
    os.remove("session_features.csv")
    os.remove("command_features.csv")
    os.remove("campaign_analysis.csv")
    os.remove("cluster_features.csv")
    os.remove("cluster_features.csv.json")

    print("unit test: OK")
