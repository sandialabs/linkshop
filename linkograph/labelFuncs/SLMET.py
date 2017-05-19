#!/usr/bin/env python3

"""The SLMET package implements the SLMET abs class labeling.

The SLMET package implements the SLMET abstraction classes labeling
via regular expressions. Label rules are of the form (cmd pattern, arg
pattern). Rules can be combined such as (cmd pattern, arg
pattern)&(cmd patter, arg pattern) When rules are combined, they
represent a label that represents a sequence of commands. For example,
('dir', '.*')&('ping', '.*') matches the sequence of commands
    dir
    ping
but does not match
    dir
    ifconfig
    ping.

"""

import re # For regular expressions

def regExLook(event, event_num, eventList):
    """Applies regex expression to determine if event is a LOOK."""
    cmdArgPairs = [(("set|query|tasklist|sc|whoami|dir|ipconfig"
                      "|ping|netstat|ver|cat|systeminfo|filever|time"
                      "|echo|type|ver"),
                     "[^>]*$"
                   ),
                   ("net",
                    ("view([\\s]+.*|$)|user([\\s]+.*|$)"
                     "|localgroup([\\s]+.*|$)|statistics([\\s]+.*|$)"
                     "|group([\\s]+.*|$)|share([\\s]+.*|$)")
                   ),
                   ("reg", "query([\\s]+.*|$)"),
                   ( ".*\\.vbs", "get([\\s]+.*|$)|enum([\\s]+.*|$)"),
                   (("set|dir|tasklist|ipconfig|ver|systeminfo"
                     "|whoami|hostname"),
                    ""
                   )]


    matched = False
    for (command, arguments) in cmdArgPairs:
        tmp = _matched(command, arguments, event)
        matched = matched | _matched(command, arguments, event)

    if matched:
        return ['Look']
    else:
        return []
    
def regExTransfer(event, event_num, eventList):
    """Applies regex expression to determine if event is a TRANSFER."""
    cmdArgPairs = [("download|ftp|upload|scp", ".*"),
                   ("net", "use([\\s]+.*|$)")]

    matched = False
    for (command, arguments) in cmdArgPairs:
        tmp = _matched(command, arguments, event)
        matched = matched | _matched(command, arguments, event)

    if matched:
        return ['Transfer']
    else:
        return []

def regExExecute(event, event_num, eventList):
    """Applies regex expression to determine if event is a EXECUTE."""
    cmdArgPairs = [(".*exe|cscript", ".*"),
                   ("net", "start([\\s]+.*|$)")]

    matched = False
    for (command, arguments) in cmdArgPairs:
        tmp = _matched(command, arguments, event)
        matched = matched | _matched(command, arguments, event)

    if matched:
        return ['Execute']
    else:
        return []

def regExMove(event, event_num, eventList):
    """Applies regex expression to determine if event is a MOVE."""
    cmdArgPairs = [(("cd|copy|ren|move|mkdir|wmic|osql|taskkill|at"
                     "|schtask|regedit"),
                    ".*"),
                   (".*\\.vbs", "set([\\s]+.*|$)"),
                   ("reg", "delete([\\s]+.*|$)"),
                   (".*", ".*>.*")]

    matched = False
    for (command, arguments) in cmdArgPairs:
        tmp = _matched(command, arguments, event)
        matched = matched | _matched(command, arguments, event)

    if matched:
        return ['Move']
    else:
        return []

def regExCleanup(event, event_num, eventList):
    """Applies regex expression to determine if event is a CLEANUP."""
    cmdArgPairs = [("del|erase|rm", ".*"),
                   (".*\\.pskill", ".*")]

    matched = False
    for (command, arguments) in cmdArgPairs:
        tmp = _matched(command, arguments, event)
        matched = matched | _matched(command, arguments, event)

    if matched:
        return ['Cleanup']
    else:
        return []

def regExShell(event, event_num, eventList):
    """Applies regex expression to determine if event is a SHELL."""
    cmdArgPairs = [("cmd.exe",".*")]

    matched = False
    for (command, arguments) in cmdArgPairs:
        tmp = _matched(command, arguments, event)
        matched = matched | _matched(command, arguments, event)

    if matched:
        return ['Access']
    else:
        return []


######################################################################
#------------------------- internal functions ------------------------

def _matched(commandRegEx, argsRegEx, event):
    """Determines if event satisfies supplied regular expressions."""

    cmdSplit = event.split(None, 1)

    cmd = cmdSplit[0]
    arg = ''
    if len(cmdSplit) > 1:
        arg = cmdSplit[1]

    return bool((re.match(commandRegEx, cmd, re.IGNORECASE) and
            re.match(argsRegEx, arg)))

######################################################################
# list of labelers
absClassLabelers = [('regExLook', regExLook),
                    ('regExTransfer', regExTransfer),
                    ('regExExecute', regExExecute),
                    ('regExMove', regExMove),
                    ('regExCleanup', regExCleanup),
                    ('regExShell', regExShell)]
