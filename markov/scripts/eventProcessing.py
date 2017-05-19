#!/usr/bin/env python3

"""Functions to manipulate data on the sessions."""

import bisect # For the bisect function.

session_counts = [167, 15, 6, 83, 8, 27, 66, 19, 17, 9, 2, 36, 46, 55,
                  6, 6, 25, 8, 18, 12, 12, 5, 102, 12, 5, 105, 12, 5,
                  70, 1, 4, 20, 7, 20, 61, 26, 21, 41, 16, 12, 4, 16,
                  35, 5, 39, 133, 51, 8, 61, 8, 61, 8, 48 ]

cumulative_counts = [167, 182, 188, 271, 279, 306, 372, 391, 408, 417,
                     419, 455, 501, 556, 562, 568, 593, 601, 619,
                     631, 643, 648, 750, 762, 767, 872, 884, 889,
                     959, 960, 964, 984, 991, 1011, 1072, 1098, 1119,
                     1160, 1176, 1188, 1192, 1208, 1243, 1248, 1287,
                     1420, 1471, 1479, 1540, 1548, 1609, 1617, 1665]

######################################################################

# Note that this function uses the session_counts module variable.
def session_count_to_total_count(session, session_count):
    """Convert event count in session to event count in total.

    Note that all events are zero indexed.

    inputs:

    session: the session number.

    session_count: the event count in the session.

    output:

    the event count from the beginning.

    """

    # subtract 1 from session, since sessions are 1 index, but the
    # arrays are zero indexed.
    session = session - 1

    if session_count < 0 or session_count >= session_counts[session]:
        raise ValueError("{0} is out of range for Session"
                         " {1}".format(session_count, session))

    
    previous_events = sum(session_counts[:session])

    return previous_events + session_count

# Note that this cumulative_counts module variable.
def total_count_to_session_count(total_count):
    """Convert total event count to session and session count.

    Note that all events are zero indexed.


    inputs:

    total_count: the total event count.

    returns: (session, session_count)

    session: the session number.

    session_count: event count in session.

    """

    if total_count >= cumulative_counts[-1] or total_count < 0:
        raise ValueError("{0} is out of range."
                         " Events are 0 to 1664.".format(total_count))


    # Find the index in cumulative_counts where total_count would be
    # placed. This finds the session index number.
    session_index = bisect.bisect_right(cumulative_counts,
                                        total_count)

    # Since sessions are 1 indexed, add 1 to the session index.
    session = session_index + 1

    session_count = total_count

    if session_index > 0:
        session_count = session_count - cumulative_counts[session_index-1]

    return session, session_count

def create_event_annotation(total_size, graph_size, step):
    """Creates a string that provides the event locations."""

    string_form = ""

    events = list(range(0, total_size))

    for i in events[0::step]:
        current =  map(lambda x: str(total_count_to_session_count(x)), events[i:i+graph_size])

        string_form += '\nstep' + str(i) + '\n'
        string_form += '\n'.join(current)

    return string_form
