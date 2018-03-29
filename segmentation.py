import pandas as pd

# Returns the index related to the beg and end timestamp desired
def interval(time, beg, en):
    j = 0

    time = pd.to_datetime(time)
    beg = pd.to_datetime(beg)
    en = pd.to_datetime(en)
   # print "time"

    for j in range(len(time)):
       # print j
        #print time[j]
        if pd.Timestamp(time[j]) == beg:
            beginning = j

        if pd.Timestamp(time[j]) == en:
            end = j + 1
         #   print time[j]
          #  print end
            break


    interv = [beginning, end]
    return interv

# Extracts the interval of interest from the dataframe
def part_div(edaframe, time, start, end):
    part = pd.DataFrame()
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)
    try:
     interv = interval(time, start, end)  # extract the interval of interest from the time
     part = edaframe[interv[0]:interv[1]]
     print part
    # Check whether there is an exception: e.g. whether the end is not present in the df. In that case try
    # again. If it still does not work return an empty df
    except UnboundLocalError:
       print "exc"
       try:
        interv = interval(time, start, end )
        part = edaframe[interv[0]:interv[1]]
       except UnboundLocalError:
        print "deleted"
        part = pd.DataFrame()

    return part


# Extract the signal expressed from type based on the start and end timestamp in the experiment file
# If type = baseline_1, it extracts the first baseline signal
def signal_extraction_experiment_info(signal_table_path, signal_name, info_file_path, type):
    # Read the signal table and extract only the raw and the time
    signal_db = pd.read_csv(signal_table_path)
    signal_db_new = pd.DataFrame()
    signal_db_new[signal_name] = signal_db[signal_name]
    signal_db_new['Time'] = signal_db['Time']

    # Read the experiment info and extract start and end of the baseline_1 type
    info = pd.read_excel(info_file_path)
    duration = info[info['type'].isin([type])]

    start = pd.to_datetime(duration.start)
    end = pd.to_datetime(duration.end)

    # Segment the dataframe based on those values
    segment = part_div(signal_db_new, signal_db_new.Time, start[0], end[0])

    return segment