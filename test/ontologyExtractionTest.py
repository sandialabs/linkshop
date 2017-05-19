#!/usr/bin/env python3

import copy
import datetime
import json
import linkograph.labels as llabels
import linkograph.linkoCreate as llinkoCreate
import linkograph.linkoDrawSVG as llinkoDrawSVG
import linkograph.stats as lstats
import os
import sys

fp_tolerance = 0.00001

#############################################################
# extract the set of all labels from the specified linkograph
#############################################################

def create_label_set(lg):

    label_set = set()

    for node in lg:
        node_label_set = node[0].copy()
        node_label = node_label_set.pop()
        label_set.add(node_label)

    return label_set

###################################
# unit test the similarity function
# @todo relocate this in stats.py
###################################

def unit_test_similarity():

    print("unit testing similarity")

    result = True

    lg_0 = [
             ({"Execute"}, set(), {1}),
             ({"Execute"}, {0}, set()),
             ({"Look"}, set(), {3, 4}),
             ({"Look"}, {2}, {4}),
             ({"Look"}, {2, 3}, set())
           ]
    lg_1 = [
             ({"Execute"}, set(), {1}),
             ({"Execute"}, {0}, set()),
             ({"Look"}, set(), {3, 4}),
             ({"Look"}, {2}, {4}),
             ({"Look"}, {2, 3}, set())
           ]
    underlink_count, overlink_count, accuracy = lstats.similarity(lg_0, lg_1)
    if (
           0 != underlink_count
           or 0 != overlink_count
           or abs(1.0 - accuracy) > fp_tolerance
       ):
        print("similarity unit test 0 failed")
        result = False

    lg_0 = [
             ({"Execute"}, set(), {1, 2}),
             ({"Execute"}, {0}, set()),
             ({"Look"}, set(), {3, 4}),
             ({"Look"}, {2}, {4}),
             ({"Look"}, {2, 3}, set())
           ]
    lg_1 = [
             ({"Execute"}, set(), {1}),
             ({"Execute"}, {0}, set()),
             ({"Look"}, set(), {3, 4}),
             ({"Look"}, {2}, {4}),
             ({"Look"}, {2, 3}, set())
           ]
    underlink_count, overlink_count, accuracy = lstats.similarity(lg_0, lg_1)
    if (
           1 != underlink_count
           or 0 != overlink_count
           or abs(0.9 - accuracy) > fp_tolerance
       ):
        print("similarity unit test 1 failed")
        result = False

    lg_0 = [
             ({"Execute"}, set(), {1}),
             ({"Execute"}, {0}, set()),
             ({"Look"}, set(), {3, 4}),
             ({"Look"}, {2}, {4}),
             ({"Look"}, {2, 3}, set())
           ]
    lg_1 = [
             ({"Execute"}, set(), {1, 2}),
             ({"Execute"}, {0}, set()),
             ({"Look"}, set(), {3, 4}),
             ({"Look"}, {2}, {4}),
             ({"Look"}, {2, 3}, set())
           ]
    underlink_count, overlink_count, accuracy = lstats.similarity(lg_0, lg_1)
    if (
           0 != underlink_count
           or 1 != overlink_count
           or abs(0.9 - accuracy) > fp_tolerance
       ):
        print("similarity unit test 2 failed")
        result = False

    return result

###################################################################
# determine if the specified ontology links the two specified nodes
###################################################################

def is_ontologically_linked(node_0, node_1, ontology):

    result = False

    node_0_label_set = node_0[0].copy()
    node_1_label_set = node_1[0].copy()

    if len(node_0_label_set) > 1:
        print("multilabel node found:", node_0)
    if len(node_1_label_set) > 1:
        print("multilabel node found:", node_1)

    node_0_label = node_0_label_set.pop()
    node_1_label = node_1_label_set.pop()

    if node_0_label in ontology:
        if node_1_label in ontology[node_0_label]:
            result = True

    return result

######################################################################
# count the number of links the ontology predicts that are not present
######################################################################

def count_overlinks(ontology, lg):

    result = 0

    # iterate over nodes
    for node_index in range(len(lg)):
        # iterate over forelinks
        for forelink in range(node_index+1, len(lg)):
            if (
                   forelink not in lg[node_index][2]
                   and is_ontologically_linked(lg[node_index], lg[forelink], ontology)
               ):
                result += 1

    return result

######################################################################
# count the number of present links the ontology does not predict
######################################################################

def count_underlinks(ontology, lg):

    result = 0

    # iterate over nodes
    for node_index in range(len(lg)):
        # iterate over forelinks
        for forelink in range(node_index+1, len(lg)):
            if (
                   forelink in lg[node_index][2]
                   and not is_ontologically_linked(lg[node_index], lg[forelink], ontology)
               ):
                result += 1

    return result

###################################################################################
# calculate the accuracy of the given ontology with respect to the given linkograph
###################################################################################

def calculate_accuracy(ontology, lg):

    if 1 == len(lg):
        accuracy = 1.0
    else:
        overlink_count = count_overlinks(ontology, lg)
        underlink_count = count_underlinks(ontology, lg)
        possible_links = lstats.totalLinks(len(lg))
        accuracy = (possible_links - overlink_count - underlink_count) / possible_links

    return accuracy

##################################################
# add the specified rule to the specified ontology
##################################################

def add_rule(o, rule):

    if rule[0] in o:
        if rule[1] not in o[rule[0]]:
            o[rule[0]].append(rule[1])
    else:
        o[rule[0]] = [rule[1]]

    return o

#####################################################
# remove the specified rule to the specified ontology
#####################################################

def subtract_rule(o, rule):

    if rule[0] in o:
        if rule[1] in o[rule[0]]:
            o[rule[0]].remove(rule[1])

    return o

########################################################################
# extract ontology from linkograph
#
# Multiple strategies can deal with multilabel nodes. In this
# implementation, we add ontology rules to cover each source/destination
# label pair. This results in many overlinks.
########################################################################

def simple_lg_to_ontology(lg):

    extracted_ontology = dict()

    # iterate over nodes
    for node in lg:
        #if len(node[0]) > 1:
        #    print("multilabel node found:", node)
        # iterate over source labels
        for source_label in node[0]:
            # iterate over forelinks
            for forelink_index in node[2]:
                # iterate over destination labels
                for destination_label in lg[forelink_index][0]:
                    #if source_label in extracted_ontology:
                    #    if destination_label not in extracted_ontology[source_label]:
                    #        extracted_ontology[source_label].append(destination_label)
                    #else:
                    #    extracted_ontology[source_label] = [destination_label]
                    extracted_ontology = add_rule(extracted_ontology, (source_label, destination_label))

    return extracted_ontology

#########################################################################################################
# calculate the fraction of actual links over possible links in a given linkograph for a given label pair
#########################################################################################################

def calculate_presence(lg, pair):

    actual = 0
    possible = 0
    presence = 0.0

    # iterate over source nodes
    for source_index in range(len(lg)):
        # iterate over destination nodes
        for destination_index in range(source_index+1, len(lg)):
            source_label_set = lg[source_index][0].copy()
            source_label = source_label_set.pop()
            if source_label == pair[0]:
                destination_label_set = lg[destination_index][0].copy()
                destination_label = destination_label_set.pop()
                if destination_label == pair[1]:
                    possible += 1
                    if destination_index in lg[source_index][2]:
                        actual += 1

    if 0 < possible:
        presence = float(actual) / possible

    return presence

##############################################################################
# extract ontology from linkograph
#
# While the simple approach always adds a rule for a link, this approach
# analyzes the link presence for each label pair, then adds a rule if the link
# is present more often than not.
##############################################################################

def threshold_lg_to_ontology(lg):

    extracted_ontology = dict()

    label_set = create_label_set(lg)

    # iterate over source labels
    for source_label in label_set:
        # iterate over destination labels
        for destination_label in label_set:
            pair = (source_label, destination_label)
            presence = calculate_presence(lg, pair)
            if presence > 0.5:
                extracted_ontology = add_rule(extracted_ontology, (source_label, destination_label))

    return extracted_ontology

##################################################################################################################################
# determine the best rule, if any, from the specified label set to add to the specified ontology based on the specified linkograph
##################################################################################################################################

def best_rule_to_add(label_set, lg, o, old_accuracy):

    rule = ()
    accuracy = old_accuracy

    for source_label in label_set:
        for destination_label in label_set:
            if source_label in o:
                if destination_label in o[source_label]:
                    continue
            pair = (source_label, destination_label)
            temp = copy.deepcopy(o)
            temp = add_rule(temp, pair)
            new_accuracy = calculate_accuracy(temp, lg)
            if new_accuracy > accuracy:
                rule = pair
                accuracy = new_accuracy

    return rule, accuracy

#########################################################################################################################################
# determine the best rule, if any, from the specified label set to subtract from the specified ontology based on the specified linkograph
#########################################################################################################################################

def best_rule_to_subtract(lg, o, old_accuracy):

    rule = ()
    accuracy = old_accuracy

    for source_label in o:
        for destination_label in o[source_label]:
            pair = (source_label, destination_label)
            temp = copy.deepcopy(o)
            temp = subtract_rule(temp, pair)
            new_accuracy = calculate_accuracy(temp, lg)
            if new_accuracy > accuracy:
                rule = pair
                accuracy = new_accuracy

    return rule, accuracy

##########################################################################################################
# transform a linkograph and ontology into an SVG named according to the specified base_name and iteration
##########################################################################################################

def visualize(lg, o, base_name, iteration):

    # derive linkograph using labels from existing linkograph
    # @attention is there a better way to extract labeling from a linkograph?
    labeling = dict()
    for node_index in range(len(lg)):
        label_set = lg[node_index][0].copy()
        label = label_set.pop()
        if not label in labeling:
            labeling[label] = [node_index]
        else:
            labeling[label].append(node_index)
    derived_lg = llinkoCreate.createLinko(labeling, o)

    # persist image of derived linkograph
    svg = llinkoDrawSVG.linkoDrawSVG(derived_lg)
    with open(base_name + "_" + str(iteration) + ".svg", "w") as svg_file:
        svg_file.write(svg)

#################################################################################################
# make a flipbook from a series of SVGs named according to the specified base_name and iterations
#################################################################################################

def make_flipbook(base_name, iterations):

    # convert .svg to .gif
    i = 0
    while i <= iterations:
        really_base_name = base_name + "_" + str(i)
        cmd = "convert " + really_base_name + ".svg " + really_base_name + ".gif"
        os.system(cmd)
        i += 1

    # create flipbook
    cmd = "convert -delay 100 -loop 0 "
    i = 0
    while i <= iterations:
        cmd += base_name + "_" + str(i) + ".gif "
        i += 1
    cmd += base_name + "_animation.gif"
    os.system(cmd)

##############################################
# refine linkograph and ontology into ontology
##############################################

def greedy_lg_o_to_o(lg, o, base_name):

    o_prime = copy.deepcopy(o)
    iteration = 0
    visualize(lg, o_prime, base_name, iteration)
    iteration += 1

    label_set = create_label_set(lg)

    baseline_accuracy = calculate_accuracy(o_prime, lg)
    ontology_change = True
    while ontology_change:
        add_me_rule, add_me_accuracy = best_rule_to_add(label_set, lg, o_prime, baseline_accuracy)
        subtract_me_rule, subtract_me_accuracy = best_rule_to_subtract(lg, o_prime, baseline_accuracy)
        if (
               add_me_accuracy > baseline_accuracy
               or subtract_me_accuracy > baseline_accuracy
           ):
            if add_me_accuracy >= subtract_me_accuracy:
                o_prime = add_rule(o_prime, add_me_rule)
                baseline_accuracy = add_me_accuracy
            else:
                o_prime = subtract_rule(o_prime, subtract_me_rule)
                baseline_accuracy = subtract_me_accuracy
            visualize(lg, o_prime, base_name, iteration)
            iteration += 1
        else:
            ontology_change = False

    make_flipbook(base_name, iteration-1)

    return o_prime

#######################################################################################
# refine linkograph and ontology into ontology constrained by specified maximum changes
#######################################################################################

def brute_force_minimum_similarity(lg, o, maximum_changes):

    best_o = copy.deepcopy(o)
    best_accuracy = calculate_accuracy(o, lg)

    if 0 < maximum_changes:
        label_set = create_label_set(lg)

        for source_label in label_set:
            for destination_label in label_set:
                pair = (source_label, destination_label)
                o_0 = copy.deepcopy(o)
                if source_label in o:
                    if destination_label in o[source_label]:
                        o_0 = subtract_rule(o_0, pair)
                    else:
                        o_0 = add_rule(o_0, pair)
                else:
                    o_0 = add_rule(o_0, pair)
                accuracy_0 = calculate_accuracy(o_0, lg)
                o_1, accuracy_1 = brute_force_minimum_similarity(lg, o_0, maximum_changes-1)

                if accuracy_0 > best_accuracy:
                    best_o = o_0
                    best_accuracy = accuracy_0
                if accuracy_1 > best_accuracy:
                    best_o = o_1
                    best_accuracy = accuracy_1

    return best_o, best_accuracy

#####################################################################
# calculate how often a given link could appear in a given linkograph
#####################################################################

def calculate_pair_frequency(lg, pair):

    result = 0

    for source_index in range(len(lg)):
        source = lg[source_index]
        for destination_index in range(source_index+1, len(lg)):
            destination = lg[destination_index]
            source_label_set = source[0].copy()
            source_label = source_label_set.pop()
            destination_label_set = destination[0].copy()
            destination_label = destination_label_set.pop()
            if (
                   pair[0] == source_label
                   and pair[1] == destination_label
               ):
                result += 1

    return result

################################################################
# sort a list of label pairs associated with a given linkograph
# @todo this is a bubble sort, which is the worst possible thing
# @todo why pass in the pair list?
################################################################

def sort_pair_list(pair_list, lg):

    sorted_pair_list = []

    # repeat until the sorted list is complete
    while len(sorted_pair_list) < len(pair_list):

        # find highest frequency pair
        highest_pair = None
        highest_frequency = -1
        foo = [pair for pair in pair_list if pair not in sorted_pair_list]
        for pair in foo:
            frequency = calculate_pair_frequency(lg, pair)
            if frequency > highest_frequency:
               highest_pair = pair
               highest_frequency = frequency

        # append highest pair to sorted list
        sorted_pair_list.append(highest_pair)

    return sorted_pair_list

#######################################################################################
# refine linkograph and ontology into ontology constrained by specified maximum changes
#######################################################################################

def high_impact_first_minimum_similarity(lg, o, maximum_changes):

    accuracy_prime = calculate_accuracy(o, lg)
    o_prime = copy.deepcopy(o)

    if len(lg) > 1:
        if 0 < maximum_changes:
            label_set = create_label_set(lg)

            pair_list = []
            for source_label in label_set:
                for destination_label in label_set:
                    pair_list.append((source_label, destination_label))

            sorted_pair_list = sort_pair_list(pair_list, lg)

            for pair in sorted_pair_list:
                o_0 = copy.deepcopy(o_prime)
                if pair[0] in o_0:
                    if pair[1] in o_0[pair[0]]:
                        o_0 = subtract_rule(o_0, pair)
                    else:
                        o_0 = add_rule(o_0, pair)
                else:
                    o_0 = add_rule(o_0, pair)

                accuracy_0 = calculate_accuracy(o_0, lg)

                if accuracy_0 > accuracy_prime:
                    maximum_changes -= 1
                    accuracy_prime = accuracy_0
                    o_prime = o_0
                    if 0 == maximum_changes:
                        break

    return o_prime, accuracy_prime

###############################################################################
# refine linkograph and ontology into ontology based on k length sublinkographs
###############################################################################

def windowed_refinement(lg, o, k):

    o_prime = copy.deepcopy(o)

    label_set = create_label_set(lg)

    for sublg_index in range(len(lg) - k + 1):
        sublg = llinkoCreate.createSubLinko(lg, sublg_index, sublg_index+k-1)
        best_rule = None
        best_accuracy = calculate_accuracy(o_prime, sublg)
        for source_label in label_set:
            for destination_label in label_set:
                pair = (source_label, destination_label)
                o_0 = copy.deepcopy(o_prime)
                if source_label in o_prime:
                    if destination_label in o_prime[source_label]:
                        o_0 = subtract_rule(o_0, pair)
                    else:
                        o_0 = add_rule(o_0, pair)
                else:
                    o_0 = add_rule(o_0, pair)
                accuracy_0 = calculate_accuracy(o_0, sublg)
                if accuracy_0 > best_accuracy:
                    best_rule = pair
                    best_accuracy = accuracy_0
        if best_rule:
            if best_rule[0] in o_prime:
                if best_rule[1] in o_prime[best_rule[0]]:
                    o_prime = subtract_rule(o_prime, best_rule)
                else:
                    o_prime = add_rule(o_prime, best_rule)
            else:
                o_prime = add_rule(o_prime, best_rule)

    return o_prime

###############################################################################
# refine linkograph and ontology into ontology based on k length sublinkographs
###############################################################################

def converging_windowed_refinement(lg, o, k):

    o_prime = windowed_refinement(lg, o, k)
    o_prime_prime = windowed_refinement(lg, o_prime, k)
    while o_prime != o_prime_prime:
        o_prime = o_prime_prime
        o_prime_prime = windowed_refinement(lg, o_prime, k)

    return o_prime

################################################
# unit test the simple implementation
################################################

def unit_test_simple():

    print("unit testing simple")

    result = True

    lg_items = [
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
    lg = llinkoCreate.Linkograph(lg_items)

    perfect_ontology = {
                           "Look": ["Transfer"],
                           "Transfer": ["Move"],
                           "Move": ["Execute"],
                           "Execute": ["Cleanup"],
                           "Cleanup": ["Look"]
                       }
    o = simple_lg_to_ontology(lg)
    if o != perfect_ontology:
        print("simple unit test 0 failed")
        result = False

    return result

################################################
# unit test the threshold implementation
################################################

def unit_test_threshold():

    print("unit testing threshold")

    result = True

    lg_items = [
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
    lg = llinkoCreate.Linkograph(lg_items)

    perfect_ontology = {
                           "Look": ["Transfer"],
                           "Transfer": ["Move"],
                           "Move": ["Execute"],
                           "Execute": ["Cleanup"],
                           "Cleanup": ["Look"]
                       }
    o = threshold_lg_to_ontology(lg)
    if o != perfect_ontology:
        print("threshold unit test 0 failed")
        result = False

    return result

################################################
# unit test the greedy refinement implementation
################################################

def unit_test_greedy():

    print("unit testing greedy refinement")

    result = True

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

    perfect_ontology = {
                           "Look": ["Transfer"],
                           "Transfer": ["Move"],
                           "Move": ["Execute"],
                           "Execute": ["Cleanup"],
                           "Cleanup": ["Look"]
                       }
    o_prime = greedy_lg_o_to_o(lg_0, perfect_ontology, "perfect")
    if o_prime != perfect_ontology:
        print("greedy unit test 0 failed")
        result = False

    null_ontology = {}
    o_prime = greedy_lg_o_to_o(lg_0, null_ontology, "null")
    if o_prime != perfect_ontology:
        print("greedy unit test 1 failed")
        result = False

    complete_ontology = {
                            "Look": ["Look", "Transfer", "Move", "Execute", "Cleanup"],
                            "Transfer": ["Look", "Transfer", "Move", "Execute", "Cleanup"],
                            "Move": ["Look", "Transfer", "Move", "Execute", "Cleanup"],
                            "Execute": ["Look", "Transfer", "Move", "Execute", "Cleanup"],
                            "Cleanup": ["Look", "Transfer", "Move", "Execute", "Cleanup"]
                        }
    o_prime = greedy_lg_o_to_o(lg_0, complete_ontology, "complete")
    if o_prime != perfect_ontology:
        print("greedy unit test 2 failed")
        result = False

    return result

######################################################################
# profile the brute force minimum similarity refinement implementation
######################################################################

def profile_bfms():

    print("profiling brute force minimum similarity")

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

    null_ontology = {}

    for maximum_changes in range(1, 4):
        start_datetime = datetime.datetime.now()
        o_prime, accuracy_prime = brute_force_minimum_similarity(lg_0, null_ontology, maximum_changes)
        end_datetime = datetime.datetime.now()
        run_datetime = end_datetime - start_datetime
        print("  maximum changes =", maximum_changes, "runtime:", run_datetime)
        # @todo instrument a real unit test for BFMS (e.g., ensure output ontology is sufficiently similar to input ontology)

##############################################################################
# unit test the high impact first minimum similarity refinement implementation
##############################################################################

def unit_test_hifms():

    print("unit testing high impact first minimum similarity")

    result = True

    perfect_ontology = {
                           "Look": ["Transfer"],
                           "Transfer": ["Move"],
                           "Move": ["Execute"],
                           "Execute": ["Cleanup"],
                           "Cleanup": ["Look"]
                       }
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

    null_ontology = {}

    for maximum_changes in range(1, 6):
        start_datetime = datetime.datetime.now()
        o_prime, accuracy_prime = high_impact_first_minimum_similarity(lg_0, null_ontology, maximum_changes)
        end_datetime = datetime.datetime.now()
        run_datetime = end_datetime - start_datetime
        print("  maximum changes =", maximum_changes, "runtime:", run_datetime)
        if maximum_changes >= 5:
            if o_prime != perfect_ontology:
                print("hifms unit test 0 failed")
                result = False

    complete_ontology = {
                            "Look": ["Look", "Transfer", "Move", "Execute", "Cleanup"],
                            "Transfer": ["Look", "Transfer", "Move", "Execute", "Cleanup"],
                            "Move": ["Look", "Transfer", "Move", "Execute", "Cleanup"],
                            "Execute": ["Look", "Transfer", "Move", "Execute", "Cleanup"],
                            "Cleanup": ["Look", "Transfer", "Move", "Execute", "Cleanup"]
                        }

    for maximum_changes in range(1, 21):
        start_datetime = datetime.datetime.now()
        o_prime, accuracy_prime = high_impact_first_minimum_similarity(lg_0, complete_ontology, maximum_changes)
        end_datetime = datetime.datetime.now()
        run_datetime = end_datetime - start_datetime
        print("  maximum changes =", maximum_changes, "runtime:", run_datetime)
        if maximum_changes >= 20:
            if o_prime != perfect_ontology:
                print("hifms unit test 1 failed")
                result = False

    return result

##################################################
# unit test the windowed refinement implementation
##################################################

def unit_test_windowed_refinement():

    print("unit testing windowed refinement")

    result = True

    perfect_ontology = {
                           "Look": ["Transfer"],
                           "Transfer": ["Move"],
                           "Move": ["Execute"],
                           "Execute": ["Cleanup"],
                           "Cleanup": ["Look"]
                       }
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

    null_ontology = {}

    for k in range(2, 7):
        o_prime = windowed_refinement(lg_0, null_ontology, k)
        if o_prime != perfect_ontology:
            print("windowed refinement unit test 0 failed")
            result = False

    complete_ontology = {
                            "Look": ["Look", "Transfer", "Move", "Execute", "Cleanup"],
                            "Transfer": ["Look", "Transfer", "Move", "Execute", "Cleanup"],
                            "Move": ["Look", "Transfer", "Move", "Execute", "Cleanup"],
                            "Execute": ["Look", "Transfer", "Move", "Execute", "Cleanup"],
                            "Cleanup": ["Look", "Transfer", "Move", "Execute", "Cleanup"]
                        }

    # k = 2: 0 rules removed
    # k = 3: 5 rules removed
    # k = 4: 7 rules removed
    # k = 5: 6 rules removed
    # k = 6: 5 rules removed
    # k = 7: 4 rules removed
    # k = 8: 3 rules removed
    # k = 9: 2 rules removed
    # k = 10: 1 rule removed
    for k in range(2, 12):
        o_prime = windowed_refinement(lg_0, complete_ontology, k)

    return result

def unit_test_converging_windowed_refinement():

    print("unit testing converging windowed refinement")

    result = True

    perfect_ontology = {
                           "Look": ["Transfer"],
                           "Transfer": ["Move"],
                           "Move": ["Execute"],
                           "Execute": ["Cleanup"],
                           "Cleanup": ["Look"]
                       }
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

    null_ontology = {}

    for k in range(2, 11):
        o_prime = converging_windowed_refinement(lg_0, null_ontology, k)
        if o_prime != perfect_ontology:
            print("converging windowed refinement unit test 0 failed for k =", k)
            result = False

        complete_ontology = {
                                "Look": ["Look", "Transfer", "Move", "Execute", "Cleanup"],
                                "Transfer": ["Look", "Transfer", "Move", "Execute", "Cleanup"],
                                "Move": ["Look", "Transfer", "Move", "Execute", "Cleanup"],
                                "Execute": ["Look", "Transfer", "Move", "Execute", "Cleanup"],
                                "Cleanup": ["Look", "Transfer", "Move", "Execute", "Cleanup"]
                            }
        o_prime = converging_windowed_refinement(lg_0, complete_ontology, k)
        if k > 5:
            if o_prime != perfect_ontology:
                print("converging windowed refinement unit test 1 failed for k =", k)
                print(o_prime)
                result = False

    return result

if "__main__" == __name__:

    if False == unit_test_similarity():
        exit()

    if False == unit_test_simple():
        exit()

    if False == unit_test_threshold():
        exit()

    if False == unit_test_greedy():
        exit()

    if False == profile_bfms():
        exit()

    if False == unit_test_hifms():
        exit()

    if False == unit_test_windowed_refinement():
        exit()

    if False == unit_test_converging_windowed_refinement():
        exit()

    print("unit test: OK")

    if 1 >= len(sys.argv):
        exit()

    session_filename = sys.argv[1]

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
    labeling = json.load(inv_labeling_file)
    lg = llinkoCreate.createLinko(labeling, json.load(ontology_file))
    inv_labeling_file.close()
    ontology_file.close()

    # a linkograph is a list of tuples (nodes)
    # a node is a 3-tuple
    # component 0 is a set of labels
    # component 1 is a set of backlinks
    # component 2 is a set of forelinks

    ##################################
    # transform linkograph to ontology
    ##################################

    extracted_ontology = simple_lg_to_ontology(lg)

    ##################################
    # calculate under/overlink metrics
    ##################################

    inv_labeling_file = open("labeled.json", "r")
    lg_prime = llinkoCreate.createLinko(json.load(inv_labeling_file), extracted_ontology)
    inv_labeling_file.close()
    underlink_count, overlink_count, accuracy = lstats.similarity(lg, lg_prime)
    print(sys.argv[1], "extracted ontology yields", underlink_count, "underlinks,", overlink_count, "overlinks and", accuracy, "accuracy")

    #########
    # cleanup
    #########

    os.remove("labeled.json")
