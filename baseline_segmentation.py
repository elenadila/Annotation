import pandas as pd
import numpy as np
import random
import segmentation
from matplotlib import pyplot as plt
from database_creation import add_feature_to_db
from database_creation import create_feature_from_segment, segment_episodes
from datetime import timedelta

# Counts the number of laughter episodes from the laughter_annotation.txt file
def num_episodes(laughter_file):
    annotation_db = pd.read_csv(laughter_file,delimiter="\t")
    n_episodes = len(annotation_db.duration.values)
    return n_episodes

# Generate segments from the signal. The beginning of the segment is randomly selected. The seed for the random is incremented every
#time a new segment is generated. In this way we should be sure that the all the signals baseline segments are computed from the same segment.
# window_length is the number of seconds we want for the segments
def random_segment(trace, signal_name, seed, window_length):
  #  random.seed(seed)

    beg_segm = random.randint(0,len(trace)) # randomly generate the beg of the segment

    len_interval = 0
    print trace
    # Check the signal and adjust the interval len based on the sampling rate of each signal
    if signal_name == 'EDA':
        len_interval = 4
    if signal_name == 'TEMP':
        len_interval = 4
    if signal_name == 'BVP':
        len_interval = 64
    if signal_name == 'HR':
        len_interval = 1
    if signal_name == 'ACC':
        len_interval = 32

    end_segm = beg_segm + len_interval * window_length

    try:
     b = pd.to_datetime(trace.Time.iloc[beg_segm])

     leng = float( (pd.to_datetime(trace.Time.iloc[end_segm])  - b).total_seconds())
    except IndexError:
        print "E1"
        beg_segm = random.randint(0,len(trace))
        end_segm = beg_segm + len_interval * window_length


        b = pd.to_datetime(trace.Time.iloc[beg_segm])

        leng = float((pd.to_datetime(trace.Time.iloc[end_segm]) - b).total_seconds())

    print "LENGHT"
    print leng
    while (leng > 4.0):
        beg_segm = random.randint(0,len(trace)-1)
        end_segm = beg_segm + len_interval * window_length

        print "OK"
 #   if end_segm - beg_segm > 4:
    # Extract the Time Series of the interval of interest
        try:
         b = pd.to_datetime(trace.Time.iloc[beg_segm])
         print b
         leng = float((pd.to_datetime(trace.Time.iloc[end_segm]) - b).total_seconds())
         print leng
        except IndexError:
            print "ERROR"


            beg_segm = random.randint(0, len(trace) - window_length*len_interval)
            end_segm = beg_segm + len_interval * window_length


            b = pd.to_datetime(trace.Time.iloc[beg_segm])
            print b
            print trace.Time
            leng = float((pd.to_datetime(trace.Time.iloc[end_segm]) - b).total_seconds())
            print leng
    time_segm = trace.Time.iloc[beg_segm:end_segm]
    print "LAST"
    print time_segm
  # We have to consider the IBI separately since it does not have a sampling rate
  #   if signal_name == 'IBI':
  #       time_segm_start = trace.Time.iloc[beg_segm]
  #       # for the end of the segment we consider the timestamp, from it we have then to extract the indices
  #       time_segm_end = str(pd.to_datetime(time_segm_start) + timedelta(seconds= window_length))
  #       time_array = trace.Time.values
  #       # extract the index of the end timestamp
  #       for cont in range(0, len(time_array)):
  #           if time_array[cont] == time_segm_end:
  #            end_segm = cont
  #
  #      # Extract the Time Series of the segment
  #       time_segm = trace.Time.iloc[beg_segm:end_segm]

    # If the it is empty, try to change the beginning of the segment and run again the previous procedure until the segment is not empty
    while time_segm.empty:
        print "EMPTY"
        beg_segm = random.randint(0, len(trace))
        try:
         time_segm_start = trace.Time.iloc[beg_segm]
        except IndexError:
            print "E3"
        time_segm_end = str(pd.to_datetime(time_segm_start) + timedelta(seconds= window_length))
        time_array = trace.Time.values
        for cont in range(0, len(time_array)):
            if time_array[cont] == time_segm_end:
                end_segm = cont

                time_segm = trace.Time.iloc[beg_segm:end_segm]
        print time_segm

    return [time_segm, beg_segm,end_segm]


# Create all the segments
def random_segments(num_episodes, sign_name, signal_table_path,sign_bas ):
    signal_db = pd.read_csv(signal_table_path)
    signal_db_new = pd.DataFrame()
    signal_db_new[sign_name] = signal_db[sign_name]
    signal_db_new['Time'] = signal_db['Time']
    random_traces = []
   # print num_episodes
    segm =0
    start_random = []
    end_random = []
    segm_index = []
    for i in range(0, num_episodes):
       # #for j in range(1, len(num_episodes())):
       # sign_bas = sign_bas[start_random[i]:end_random[i]]
        [segm, b, e] = random_segment(sign_bas, sign_name,i, 3)
        sign_bas = sign_bas.drop(sign_bas.index[b:e])
        ### TODO: exclude the already used intervals from the dataframe: sign_bas.iloc[b:e] is the already used dataset

        print " TEST"
        print sign_bas.drop(sign_bas.index[b:e])
        rand_segm = segmentation.part_div(signal_db_new, signal_db_new.Time, segm.iloc[0], segm.iloc[len(segm)-1])

            #  print len(rand_segm)
        start_random.append(segm.iloc[0])
        end_random.append(segm.iloc[len(segm)-1])
        random_traces.append(rand_segm[sign_name])
        segm_index.append(segm)
  #  print "index"
   # print segm_index
    return [random_traces, start_random, end_random]




if __name__ == '__main__':
    dir = "C:\Users\user\Desktop\Pilot_Study/"
    user = 'u001/'
    signals = ['EDA', 'BVP', 'HR', 'TEMP', 'ACC']
    #components = ['EDA', 'BVP', 'HR', 'TEMP', 'ACC', 'IBI']

    hands = ['right', 'left']
    laughter_annotation_file = '/laughter_annotation.txt'
    user_loc = dir + user
    info_file = 'experiment_info.xlsx'
  #  print num_episodes(dir + user + laughter_annotation_file)
    for p in range(0, len(signals)):
        for j in range(0, len(hands)):
            baseline =  segmentation.signal_extraction_experiment_info(dir + user +hands[j] + '/' + signals[p] + '_Table.csv',
                                                                       signals[p], dir + user +info_file, 'baseline_1')
         #   print baseline
           # segm_trac =  random_segment(baseline,signals[p])
        #    print segm_trac
            [baseline_traces, start_seg, end_seg] = random_segments(num_episodes(dir + user + laughter_annotation_file),
                                  signals[p],dir + user +hands[j] + '/' + signals[p] + '_Table.csv', baseline)

       #     [t, s, e, id, d] = segment_episodes(dir, user, hands[j], signals[p], laughter_annotation_file)

            add_feature_to_db(user_loc, hands[j], 'start', start_seg, 'Baseline')
            add_feature_to_db(user_loc, hands[j], 'end', end_seg, 'Baseline')
            add_feature_to_db(user_loc, hands[j], 'laugter_id', id, 'Baseline')
            add_feature_to_db(user_loc, hands[j],'duration', [3]*len(start_seg), 'Baseline')
            add_feature_to_db(user_loc, hands[j],'hand', hands[j], 'Baseline')
            add_feature_to_db(user_loc, hands[j], 'user_ID', [user[0:len(user)-1]]*len(start_seg), 'Baseline')
            add_feature_to_db(user_loc, hands[j], 'type', ['baseline'] * len(start_seg), 'Baseline')
          #  mean = create_feature_from_segment(baseline,np.mean)
           # add_feature_to_db(user_loc,hands[j],'mean_' + signals[p],mean, 'Baseline')
            print signals[p]

            mean = create_feature_from_segment(baseline_traces,np.mean)
            add_feature_to_db(user_loc,hands[j],'mean_' + signals[p],mean, 'Baseline')
            std = create_feature_from_segment(baseline_traces, np.std)
            add_feature_to_db(user_loc, hands[j], 'std_' + signals[p], std, 'Baseline')


