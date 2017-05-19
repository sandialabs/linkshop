#!/usr/bin/env python3

import labels
import linkoCreate

label = labels.labelCommands('trial.json', 'labelRule2.json', 'out.json',
                             'noLabel')

print(label)
