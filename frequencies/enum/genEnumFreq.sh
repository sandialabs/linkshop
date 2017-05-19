#!/usr/bin/bash

######################################################################
#
# The script is a simple wrapper for the frequency.py function with
# using enum option. It finds the number of distinct linkographs that
# can be derived from a given ontology for a given number of
# nodes. The linkographs are given in terms of their enum encoding.
#
# usage-
#    ./genEnumFreq.sh <max number of nodes> <ontology> <file name>
#
# Arguments-
#    <max number of nodes> -- the maximum number of nodes to consider.
#    <ontology>  -- The ontology to use.
#    <file name> -- the base name for printing the results. The files
#    are named <file name>n.csv where n is the number of
#    nodes.
#
######################################################################

usage(){
echo 'usage-'
echo '   ./genEnumFreq.sh <max number of nodes> <ontology> <file name>'
echo
echo 'Arguments-'
echo '   <max number of nodes> -- the maximum number of nodes to consider.'
echo '   <ontology>  -- The ontology to use.'
echo '   <file name> -- the base name for printing the results. The files'
echo '   are named <file name>n.csv where n is the number of'
echo '   nodes.'
}

if [[ $# -ne 3 ]]; then
    usage
fi

iterations=$1
ontology=$2
basename=$3

# The enum function is the default behavior for the frequency
# function, but the enum option is used explicitly instead.

for (( n=0; n<=${iterations}; n++ )); do
    frequency.py -f enum ${n} ${ontology} > ${basename}${n}.csv
done
