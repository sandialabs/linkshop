#!/usr/bin/env python3

import json
import loadPath  # Adds the project path.
import linkograph.linkoCreate as llinkoCreate
import linkograph.stats as lstats
import ontologyExtraction as oe

"""
An abstraction transforms commands into labels.
An ontology transforms labels into a linkograph.
"""

def summarize_results(ontology, linkograph, narrative):

    overlink_count = oe.count_overlinks(ontology, linkograph)
    underlink_count = oe.count_underlinks(ontology, linkograph)
    possible_links = lstats.totalLinks(len(linkograph))
    accuracy = (possible_links - underlink_count - overlink_count) / possible_links

    print(
           narrative,
           "implementation yields:",
           overlink_count,
           "overlinks,",
           underlink_count,
           "underlinks and",
           accuracy,
           "accuracy"
         )

if "__main__" == __name__:

    # a perfect match ontology is possible with this linkograph
    # simple and threshold implementations perform perfectly
    lg_0_items = [
                     ({"Look"}, set(), {1, 6}),
                     ({"Transfer"}, set(), {2, 7}),
                     ({"Move"}, set(), {3, 8}),
                     ({"Execute"}, set(), {4, 9}),
                     ({"Cleanup"}, set(), {5}),
                     ({"Look"}, set(), {6}),
                     ({"Transfer"}, set(), {7}),
                     ({"Move"}, set(), {8}),
                     ({"Execute"}, set(), {9}),
                     ({"Cleanup"}, set(), set())
                 ]
    lg_0 = llinkoCreate.Linkograph(lg_0_items)
    # persist linkograph to JSON for visualization
    llinkoCreate.writeLinkoJson(lg_0, "lg_0.json")
    # calculate the ontologies
    o_0 = oe.simple_lg_to_ontology(lg_0)
    summarize_results(o_0, lg_0, "simple")
    out_file = open("extracted_ontology_simple_lg_0.json", "w")
    json.dump(o_0, out_file, indent=4)
    out_file.close()
    o_0 = oe.threshold_lg_to_ontology(lg_0)
    summarize_results(o_0, lg_0, "threshold")
    out_file = open("extracted_ontology_threshold_lg_0.json", "w")
    json.dump(o_0, out_file, indent=4)
    out_file.close()

    # no perfect match ontology is possible
    # the simple implementation achieves 82% accuracy
    # the threshold implementation achieves 91% accuracy
    lg_1_items = [
                     ({"Look"}, set(), set()),
                     ({"Transfer"}, set(), set()),
                     ({"Move"}, set(), set()),
                     ({"Execute"}, set(), set()),
                     ({"Cleanup"}, set(), set()),
                     ({"Look"}, set(), {6}),
                     ({"Transfer"}, set(), {7}),
                     ({"Move"}, set(), {8}),
                     ({"Execute"}, set(), {9}),
                     ({"Cleanup"}, set(), set())
                 ]
    lg_1 = llinkoCreate.Linkograph(lg_1_items)
    # persist linkograph to JSON for visualization
    llinkoCreate.writeLinkoJson(lg_1, "lg_1.json")
    # calculate the ontologies
    o_1 = oe.simple_lg_to_ontology(lg_1)
    summarize_results(o_1, lg_1, "simple")
    out_file = open("extracted_ontology_simple_lg_1.json", "w")
    json.dump(o_1, out_file, indent=4)
    out_file.close()
    o_1 = oe.threshold_lg_to_ontology(lg_1)
    summarize_results(o_1, lg_1, "threshold")
    out_file = open("extracted_ontology_threshold_lg_1.json", "w")
    json.dump(o_1, out_file, indent=4)
    out_file.close()

    # no perfect match ontology is possible
    # the simple implementation achieves 91% accuracy
    # the threshold implementation achieves 91% accuracy
    lg_2_items = [
                     ({"Look"}, set(), {1, 6}),
                     ({"Transfer"}, set(), {2, 7}),
                     ({"Move"}, set(), {3, 8}),
                     ({"Execute"}, set(), {4, 9}),
                     ({"Cleanup"}, set(), {5}),
                     ({"Look"}, set(), set()),
                     ({"Transfer"}, set(), set()),
                     ({"Move"}, set(), set()),
                     ({"Execute"}, set(), set()),
                     ({"Cleanup"}, set(), set())
                 ]
    lg_2 = llinkoCreate.Linkograph(lg_2_items)
    # persist linkograph to JSON for visualization
    llinkoCreate.writeLinkoJson(lg_2, "lg_2.json")
    # calculate the ontologies
    o_2 = oe.simple_lg_to_ontology(lg_2)
    summarize_results(o_2, lg_2, "simple")
    out_file = open("extracted_ontology_simple_lg_2.json", "w")
    json.dump(o_2, out_file, indent=4)
    out_file.close()
    o_2 = oe.threshold_lg_to_ontology(lg_2)
    summarize_results(o_2, lg_2, "threshold")
    out_file = open("extracted_ontology_threshold_lg_2.json", "w")
    json.dump(o_2, out_file, indent=4)
    out_file.close()
