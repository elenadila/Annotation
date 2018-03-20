import pandas as pd
import numpy as np
import random
import segmentation
from matplotlib import pyplot as plt
from database_creation import add_feature_to_db
from database_creation import create_feature_from_segment, segment_episodes
from datetime import timedelta
# Counts the number of laughter episodes
def num_episodes(laughter_file):
    annotation_db = pd.read_csv(laughter_file,delimiter="\t")
    n_episodes = len(annotation_db.duration.values)
    return n_episodes

# Generate
def random_segment(trace, signal_name, seed, window):
    random.seed(seed)
    len_interval = 0
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
    beg_segm = random.randint(0, len(trace) - len(trace.iloc[len_interval]))

        # if signal_name == 'IBI':
    #    len_interval = 1

    end_segm = beg_segm + len_interval*window
 #   print beg_segm
   # print end_segm

    time_segm = trace.Time.iloc[beg_segm:end_segm]


    if signal_name == 'IBI':
        time_segm_start = trace.Time.iloc[beg_segm]
        time_segm_end = str(pd.to_datetime(time_segm_start) + timedelta(seconds=window))
        time_array = trace.Time.values
        for cont in range(0, len(time_array)):
            if time_array[cont] == time_segm_end:
             end_segm = cont

       # end_segm = trace.Time.index()
             time_segm = trace.Time.iloc[beg_segm:end_segm]

    while time_segm.empty:
        beg_segm = random.randint(0, len(trace)-len(trace.iloc[len_interval]))

        time_segm_start = trace.Time.iloc[beg_segm]
        time_segm_end = str(pd.to_datetime(time_segm_start) + timedelta(seconds=window))
        time_array = trace.Time.values
        for cont in range(0, len(time_array)):
            if time_array[cont] == time_segm_end:
                end_segm = cont

                # end_segm = trace.Time.index()
                time_segm = trace.Time.iloc[beg_segm:end_segm]
#    print len(trace.Time.values)
        print time_segm
#print len(time_segm)


    return time_segm


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
    for i in range(0, num_episodes):
        segm = random_segment(sign_bas, sign_name,i, 3)

        rand_segm = segmentation.part_div(signal_db_new, signal_db_new.Time, segm.iloc[0], segm.iloc[len(segm)-1])

            #  print len(rand_segm)
        start_random.append(segm.iloc[0])
        end_random.append(segm.iloc[len(segm)-1])
        random_traces.append(rand_segm[sign_name])
        print rand_segm[sign_name]
    return [random_traces, start_random, end_random]




if __name__ == '__main__':
    dir = "C:\Users\user\Desktop\Pilot_Study/"
    user = 'u001/'
    signals = ['EDA', 'BVP', 'HR', 'TEMP', 'ACC', 'IBI']
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