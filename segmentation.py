import pandas as pd
from datetime import timedelta

# Returns the index related to the beg and end timestamp desired
def interval(time, beg, en):
    j = 0;
    interv = [];
    time = pd.to_datetime(time)

    for j in range(len(time)):

        if time[j] == pd.to_datetime(beg):
            beginning = j

        if time[j] == pd.to_datetime(en):
            end = j
            print end
            break


    interv = [beginning, end]
    return interv

# Extracts the interval of interest from the dataframe
def part_div(edaframe, time, start, end):
    part = pd.DataFrame()

    try:
     interv = interval(time, start, end)  # extract the interval of interest from the time
     part = edaframe[interv[0]:interv[1]]

    # Check whether there is an exception: e.g. whether the end is not present in the df. In that case try
    # again end + 1 sec. If it still does not work return an empty df
    except UnboundLocalError:
       print "exc"
       try:
        interv = interval(time, start, end + timedelta(seconds=1))
       except UnboundLocalError:
        print "deleted"
        part = pd.DataFrame()

    return part


