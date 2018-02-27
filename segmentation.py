import pandas as pd

def interval(time, beg, en):
    j = 0;
    interv = [];
    time = pd.to_datetime(time)
    for j in range(len(time)):
        if time[j] == beg:
            beginning = j
            print(beginning)
        if time[j] == en:
            end = j

    interv = [beginning, end]
    return interv


def part_div(edaframe, time, start, end):

    interv = interval(time, start, end)  # extract the interval of interest from the time
    part = edaframe[interv[0]:interv[1]]  # extract the EDA and the time values related to the interval of interest
    return part


