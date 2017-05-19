import datetime
import sys

def stringToDatetime(in_string):
    tokens = in_string.split(" ")
    in_date = tokens[0]
    in_time = tokens[1]
    # date may be MM/DD/YYYY or YYYY-MM-DD
    if "/" in in_date:
        date_tokens = in_date.split("/")
        year = date_tokens[2]
        month = date_tokens[0]
        date = date_tokens[1]
    else:
        date_tokens = in_date.split("-")
        year = date_tokens[0]
        month = date_tokens[1]
        date = date_tokens[2]
    time_tokens = in_time.split(":")
    minute = time_tokens[1]
    second = time_tokens[2]
    # time may be 24 hour or AM/PM
    hour = int(time_tokens[0])
    if "AM" == tokens[2]:
        if 12 == hour:
            hour = 0
    elif "PM" == tokens[2]:
        if 12 != hour:
            hour += 12
    return datetime.datetime(int(year), int(month), int(date), hour, int(minute), int(second))
