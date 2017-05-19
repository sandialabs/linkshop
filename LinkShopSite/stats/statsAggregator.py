'''
statsAggregator.py
Author: Jeffrey Bigg
'''

import json
import loadPath
import linkograph.stats as st
import linkograph.linkoCreate as lc


standard_args = {
  'totalLabels':st.totalLabels,
  'percentageOfEntries':st.percentageOfEntries,
  'links':st.links,
  'percentageOfLinks':st.percentageOfLinks,
  'graphEntropy':st.graphEntropy,
}
restrict_args = {
  'linkEntropy':st.linkEntropy,
  'linkTComplexity':st.linkTComplexity
}
'''
getStats
  This function (to be implemented) will take all available statistics
  that can be compliled and return them in a json format.
'''
def getStats(linkograph,lowerBound,upperBound):
  result = {}
  for f in standard_args:
    result[f] = standard_args[f](linkograph,lowerBound=lowerBound,upperBound=upperBound)
  for f in restrict_args:
    result[f] = restrict_args[f](linkograph,restrict=True,lowerBound=lowerBound,upperBound=upperBound)
  return result
