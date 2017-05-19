#!/usr/bin/bash

######################################################################
#
# The script is a simple wrapper for the frequency.py function with
# using Shannon entropy. It calculates the different possible Shannon
# entropy values (as applied to the whole graph) and the number of
# linkographs that map to that value.
#
# usage-
#    ./genShannonFreq.sh <max number of nodes> <ontology> <file name>
#
# Arguments-
#    <max number of nodes> -- the maximum number of nodes to consier.
#    <ontology>  -- The ontology to use.
#    <file name> -- the base name for printing the results. The files
#    will be named <file name>n.{csv, json} where n is the number of
#    nodes.
#
######################################################################

usage(){
echo 'usage-'
echo '   ./genShannonFreq.sh <max number of nodes> <ontology> <file name>'
echo
echo 'Arguments-'
echo '   <max number of nodes> -- the maximum number of nodes to consier.'
echo '   <ontology>  -- The ontology to use.'
echo '   <file name> -- the base name for printing the results. The files'
echo '   will be named <file name>n.{csv, json} where n is the number of'
echo '   nodes.'
}

if [[ $# -ne 3 ]]; then
    usage
fi

iterations=$1
ontology=$2
basename=$3

for (( n=0; n<=${iterations}; n++ )); do
    frequency.py -f Shannon ${n} ${ontology} > ${basename}${n}.csv
    frequency.py -jf Shannon ${n} ${ontology} > ${basename}${n}.json
done
