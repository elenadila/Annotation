import numpy as np
import pandas as pd
import database_creation
import segmentation
import random
from datetime import timedelta
import math
import os
# Clean the Experiment_DataFrame from the required segments, specified by start and end
def clean_signal(dataframe_to_clean, start_seg, end_segm, duration):
    old = pd.DataFrame()

    # Create a DataFrame "new"  from the concat of all segments
    for i in range(0,len(start_seg)):
        print "PRINT"
        print start_seg[i]
        print end_segm[i]
        segment = segmentation.part_div(dataframe_to_clean, dataframe_to_clean.Time,
                                        start_seg[i],
                                        end_segm[i])


        new = pd.concat([segment,old])
        old = new

    # Concat the initial dataframe with the new and eliminate the duplicates
    cleaned = pd.concat([dataframe_to_clean, new]).drop_duplicates(keep=False)

    return [cleaned, duration]


# Create one baseline segment for each laughter segment. The segment will have a random beginning and the duration of
# the correspondent laughter segment
def create_baseline_segments(db_cleaned,duration_segments ):
    beg_range = len(db_cleaned)
    start = []
    end = []
    dur = []
    for i in range(0,len(duration_segments)):
        beg_segm = random.randint(0, beg_range)
        time_segm_start = pd.Timestamp((db_cleaned.Time.iloc[beg_segm])).round('1s')
        end_segm = pd.Timestamp(pd.to_datetime(time_segm_start) + timedelta(seconds=duration_segments[i])).round('1s')
        ok = 1


        # Randomly extract the beginning of the segment and check whether the segment exists in the dataframe
        # If it exists change ok to 0 and store the start and end values of the segment
        while ok:
            if (pd.to_datetime(db_cleaned.Time) == pd.to_datetime(end_segm)).any():

                start.append(time_segm_start)
                end.append(end_segm)
                dur.append((pd.to_datetime(end_segm)-pd.to_datetime(time_segm_start)).total_seconds())
                ok =0
            # If the segment doesn't exist extract another random value and check it again
            else:

              # Round the timestamp to the nearest second
                 beg_segm = random.randint(0, beg_range)
                 time_segm_start = pd.Timestamp((db_cleaned.Time.iloc[beg_segm])).round('1s')
                 end_segm = pd.Timestamp(pd.to_datetime(time_segm_start) + timedelta(seconds=duration_segments[i])).round(
                   '1s').strftime("%Y-%m-%d %H:%M:%S")
                 print "END"
                 print end_segm

              # except:
              #     print "ERROR"
              #     beg_segm = random.randint(0, beg_range)
              #     time_segm_start = pd.Timestamp((db_cleaned.Time.iloc[beg_segm])).round('1s').strftime("%Y-%M-%D %H:%M:%S")
              #     end_segm = pd.Timestamp(
              #         pd.to_datetime(time_segm_start) + timedelta(seconds=duration_segments[i])).round(
              #         '1s').strftime("%Y-%M-%D %H:%M:%S")


    return [start,end,dur]






if __name__ == '__main__':


    dir = "C:\Users\user\Desktop\Pilot_Study/"
    user = ['u001/', 'u002/', 'u003/', 'u004/', 'u005/', 'u008/']
#    user = ['u008/']
    signals = 'EDA'
    components = ['Normalized']
    hands = ['right', 'left']


# Step 1. Read the laughter annotation file and delete the laughter segments from the dataframe
# Step 2. From the cleaned file extract randomly N segments of baseline
# Step 3. Apply the functions to the segments, then store the features in the db

# for p in range(0, len(signals)):
    for u in range(0, len(user)):
        for j in range(0, len(hands)):
         for comp in range(0, len(components)):
             laughter_annotation_file = 'laughter_annotation.txt'
             additional_annotation_file = 'additional_annotation.txt'
             user_loc = dir + user[u]
             # [t, s, e, id, d, type] = database_creation.segment_episodes(dir, user[u], hands[j], signals, components[comp],
             #                                          laughter_annotation_file)

             df_additional = pd.read_csv(dir + user[u] + additional_annotation_file, delimiter="\t")
             s_add = df_additional['start_converted'].values
             e_add = df_additional['end_converted'].values
             d_add = df_additional['duration_converted'].values
             id_add = df_additional['ID'].values
             # token = df_additional[df_additional['token'] == 'cognitive_load'].token
             # print token

             df_laughter = pd.read_csv(dir + user[u] + laughter_annotation_file, delimiter="\t")
             s = df_laughter['start_converted']
             e = df_laughter['end_converted']
             d = df_laughter['duration_converted']


             df_info = pd.read_csv(dir + user[u] + "experiment_info.csv")
             start = pd.to_datetime(df_info[df_info['type'] == 'clapping'].start)
             # start = pd.to_datetime(',2018-03-09 12:03:43')
             end = pd.to_datetime(df_info[df_info['type'] == 'cognitive_load'].end)

             start = start.iloc[0]
             end = end.iloc[0]




             df_signal = pd.read_csv(dir + user[u] + hands[j] + '/' + signals + '_Table_Experiment.csv')

             s_add= np.insert(pd.to_datetime(s_add),1,pd.to_datetime(start))
             e_add= np.insert(pd.to_datetime(e_add),1,pd.to_datetime(end))

             s_add = np.concatenate((pd.to_datetime(s_add), pd.to_datetime(s)))
             e_add = np.concatenate((pd.to_datetime(e_add), (pd.to_datetime(e)+ timedelta(seconds=5))))


             print "SADD"
             print pd.to_datetime(s_add)

         #    df_signal = pd.concat([df_signal,to_remove]).drop_duplicates(keep=False)
         #
         #     [db_cleaned_add, dur_cleaned_add] = clean_signal(df_signal, pd.to_datetime(s_add),
         #                                                      pd.to_datetime(e_add),
         #                                                      d_add)
         #     #
         #     db_cleaned_add.to_csv(dir + user[u] + hands[j] + '/Test.csv',index=0)
         #     db_cleaned_add = pd.read_csv(dir + user[u] + hands[j] + '/Test.csv')
         #     os.remove(dir + user[u] + hands[j] + '/Test.csv')





             # [db_cleaned_laughter, dur_cleaned_laughter] = clean_signal(db_cleaned_add,pd.to_datetime(s),
             #                                                            pd.to_datetime(e) + timedelta(seconds=5),
             #                                                            d )
             #




             [db_cleaned_laughter, dur_cleaned_laughter] = clean_signal(df_signal,s_add,
                                                                       e_add ,
                                                                        d )

             db_cleaned_laughter.to_csv(dir + user[u] + hands[j] + '/Test.csv', index=0)

             for i in range(0,len(e_add)):
                if (pd.to_datetime(db_cleaned_laughter.Time) == pd.to_datetime(e_add[i])).any():
                    print "NOOOOOOOOO"
                    print e_add[i]


             [start_baseline, end_baseline, dur_baseline]= create_baseline_segments(db_cleaned_laughter, dur_cleaned_laughter)
             baseline_db = pd.DataFrame({'start_converted':start_baseline,'end_converted':end_baseline, 'duration_converted':dur_baseline,
                                         'ID':id,
                                         'type': ['baseline_additional_removed']*len(start_baseline)})
             baseline_db.to_csv(dir + user[u] + 'baseline_additional_removed.txt', sep="\t", index=0)
          #   dataframe_to_clean = pd.concat([df_signal, t]).drop_duplicates(keep=False)

#    print dataframe_to_clean['Time']



