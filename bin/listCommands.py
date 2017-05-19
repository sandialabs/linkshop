#!/usr/bin/env python3

"""List commands from a json."""

import argparse # For command line parsing.
import json # For parsing JSON files.

def list_command(commands, min_command=0, max_command=-1,
                 numbers=True, time=True):
    """List selected commands.

    inputs:

    commands -- The commands to list. The commands should have
    the format [ {"cmd": <command>, "ts": <timestamp>} ... ] where
    "ts" is optional.

    min_command -- The first command to list. If max_command is
    negative, then it counts from the last element in the list, just
    as is used by slicing a list. For example, min_command = -1 is the
    last command and max_command = -2 is the penultimate command. The
    default is 0.

    max_command -- The last command to list. If max_command is greater
    than the last command, then max_command acts as if it were the
    last command. If max_command is negative, then it counts from the
    last element in the list, just as is used by slicing a list. For
    example, max_command = -1 (the default) is the last command and
    max_command = -2 is the penultimate command.

    time -- If True, then timestamps are returned. If False, then
    timestamps are not returned.

    numbers -- If True, then command line numbers are included in the
    list. If False, then comman line numbers are not included.

    returns:

    A string representation of the commands where each command is
    listed on its own line and commands are separated by a blank
    line. If time is True, then the time is list on the line directly
    following the command. If numbers is True, then the command number
    is listed on the same line as the command at the first of the
    command.

    Example: If min_command is 2, max_command is 5, time is True, and
    numbers is True, then output would be:

    2 <command_2>
    <timestamp>

    3 <command_3>
    <timestamp>

    4 <command_4>
    <timestamp>

    5 <command_5>
    <timestamp>

    """

    # Adjust min_command to be positive. Need to print the correct
    # line numbers.
    if min_command < 0:
        min_command = len(commands) + min_command - 1

    # Adjust max to include the upper bound. This only needs to be
    # done (and should only be done) when max_command is non-negative.
    if max_command == -1:
        max_command = len(commands) + 1
    else:
        max_command = max_command + 1

    # Get the commands.
    commands = commands[min_command: max_command]

    # Build the string representation.
    string_commands = [
        command_string(command_dict=command_dict,
                       command_number=(command_number + min_command),
                       numbers=numbers,
                       time=time)
        for command_number, command_dict in enumerate(commands)
    ]

    string_rep = "\n".join(string_commands)

    return string_rep


# Function for formatting the command dictionary.
def command_string(command_dict, command_number=None, numbers=True,
                   time=True):
    """Create the string representation for the command entry.

    inputs:

    command_dict: A command dictionary of the form {"cmd": "<command",
    "ts": <timestamp>}. The "ts" arugment is optional.

    numbers: If true and comamnd_number is not None, then include the
    line numhber. If false, do not include the line number.

    time: If true, then include the timestamp. If false, do not
    include the timestamp.

    returns:

    A string represenation of the command.

    """
    string_rep = ""
    if numbers:
        string_rep += str(command_number) + ": "
    string_rep += command_dict["cmd"] + "\n"
    if time:
        string_rep += command_dict.get("ts", "<timestamp> missing")
        string_rep += "\n"

    return string_rep
    

if __name__ == "__main__":

    description = """Lists commands indicated from a json packaged format.  Each command
    is listed on its own line followed by the optional time
    stamp. Comands lines are separated by a line.  The default is to
    list out to the console all commands with timestamps and command
    numbers. If the timestamps do not exist, then a statement of a
    missing time stamp is listed instead."""

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("commands", metavar="COMMANDS.json",
                        help="The json file of commands to list.")

    parser.add_argument("-m", "--min-command", type=int, default=0,
                        help="The first command to list.")

    parser.add_argument("-M", "--max-command", type=int, default=-1,
                        help="The last command to list.")

    parser.add_argument("-o", "--output", metavar="OUT.json",
                        help="Write commands to OUT.json")

    parser.add_argument("-s", "--suppress-line-numbers",
                        action="store_false",
                        help="Do no print line numbers.")

    parser.add_argument("-n", "--no-time", action="store_false",
                        help="Do no print timestamps.")

    args = parser.parse_args()

    # Get the commands
    with open(args.commands, 'r') as command_file:
        commands = json.load(command_file)

    # Get the string representation
    string_rep = list_command(commands=commands,
                              min_command=args.min_command,
                              max_command=args.max_command,
                              numbers=args.suppress_line_numbers,
                              time=args.no_time)

    if args.output:
        with open(args.output, 'w') as out_file:
            out_file.write(string_rep)

    else:
        print(string_rep, end="")
