#!/usr/bin/env python3

import linkoCreate

linkograph = linkoCreate.createLinko('out.json', 'linkRules.json')

print(linkograph,)
print("Label {}".format(linkograph.labels))
print()

linkoCreate.writeLinkoJson(linkograph, 'tojson.json')

linkograph = linkoCreate.readLinkoJson('tojson.json')

print(linkograph)
