import pandas as pd
import numpy as np
import segmentation
import os
import EDA_features_extraction

""" 
    This module allows the creation of segments based on timestamp (provided from files) -segment_episodes-. 
    Compute features on the segments -create_feature_from_segment- and put them in a db -add_feature_to_db-
"""




def segment_episodes(dir, user, hand, signal,component,annotation):
    # Segments the signal based on start and end of the laughter episode

    # INPUT:
        # dir: directory of the study
        # user
        # hand
        # signal: e.g EDA, BVP, ..
        # component: e.g Phasic, Tonic
        # annotation: file for the start/end timestap

    # RETURN

        # traces: array of dataframes obtained by the part_div function
        # start: array of start_converted_timestamp
        # laughter_id
        # duration: of the segment
        # type: voiced, unvoiced, baseline of baseline_annotation_removed

    ##############################################################################################

    signal_name = signal
    # Read the laughter annotation file and store the start,end and duration of the episodes
    df_laughter = pd.read_csv(dir + user +
                              annotation, delimiter="\t")
    start = pd.to_datetime(df_laughter.start_converted.values)
    end = pd.to_datetime(df_laughter.end_converted.values)
    duration = df_laughter.duration_converted

    # Read the signal data frame
    df_signal = pd.read_csv(dir + user+ hand + '/' + signal + '_Table_Experiment.csv')
    laugher_id = df_laughter.ID.values
    type = df_laughter.type
   # print type

    traces =[]
    # Segments the signal in traces
    for i in range (0,len(start)):
        trace = segmentation.part_div(df_signal[component],df_signal.Time,start[i],end[i])
        traces.append(trace)

    return (traces, start, end, laugher_id,duration,type)

# Applies the desired function fun to the segment and returns the feature
def function_to_apply(segment, fun):

    if segment.empty:
        print "empty"
        feature = np.NaN
       # print feature
    else:
        feature = fun(segment.values)
    return feature

# Creates a feature array applying the function_to_apply to all the segments
def create_feature_from_segment(segment_traces, function):
    feat_column = []
    for i in range(0,len(segment_traces)):
        feat_column.append(function_to_apply(segment_traces[i],function))
  #  print feat_column
    return feat_column


# Add the feature_array to the database
def add_feature_to_db(user_dir,hand, feature_name, feature_column,signal_name):
    # Check if the database exists, otherwise create it
    db = check_create_db(user_dir,  hand + '_' + signal_name+ '_Database.csv')
    db_path = user_dir + hand + '_' + signal_name+ '_Database.csv'
    # Checks whether the columns already exists
    if feature_name in db.columns:
       db[feature_name] = feature_column
    # If it does not exist, it creates it
    else:
        db[feature_name] =  feature_column

    db.to_csv(db_path, index=0)

# Checks if the database exists, otherwise it creates it
def check_create_db(dirpath, filename):
 if (os.path.exists(dirpath + filename)):
            datab = pd.read_csv(dirpath + filename)
            print 'found'
 else:
         #   datab = pd.DataFrame({'user_id':[]})
            datab = pd.DataFrame({'random': []})
            datab.to_csv(filename, index=0)
           # datab = pd.read_csv(filename)
            print 'not-found'
 return datab



if __name__ == '__main__':
    dir = "C:\Users\user\Desktop\Pilot_Study/"
    user = ['u008/']
    signals = 'EDA'
    components = ['Normalized','Phasic','Tonic']
    hands = ['right','left']

    user = ['u001/', 'u002/', 'u003/', 'u004/', 'u005/', 'u008/']

    # Step 1. Divide the signal in segments: segment_episodes
    # Step 2. Add the feature column to the database - first the generic: start, end, laughter id, user id
    # Step 3. Apply the functions to the segments, then store the features in the db

  # for p in range(0, len(signals)):
    files =['/laughter_annotation.txt', '/baseline_additional_removed.txt']
    for u in range(0,len(user)):
      for ann_fil in range(0, len(files)):
       for j in range(0, len(hands)):
        for comp in range (0,len(components)):
            laughter_annotation_file = '/laughter_annotation.txt'
            user_loc = dir + user[u]

            # Step 1. Divide the signal in segments: segment_episodes
            [t, s, e ,id, d, type] = segment_episodes(dir, user[u], hands[j], signals,components[comp], files[ann_fil])
   #         # print type
   #         #  print t
   #         #  print t
   #         #  print np.mean(d)

            # Step 2. Add the feature column to the database - first the generic: start, end, laughter id, user id
            add_feature_to_db(user_loc, hands[j], 'start', s,files[ann_fil][1:9] )
            add_feature_to_db(user_loc, hands[j], 'end', e,files[ann_fil][1:9])
            add_feature_to_db(user_loc, hands[j], 'laugter_id', id,files[ann_fil][1:9])
            add_feature_to_db(user_loc, hands[j],'duration', d,files[ann_fil][1:9])
            add_feature_to_db(user_loc, hands[j],'hand', hands[j],files[ann_fil][1:9])
            add_feature_to_db(user_loc, hands[j], 'type', type, files[ann_fil][1:9])
            add_feature_to_db(user_loc, hands[j], 'user_ID', [user[u][0:len(user[u])-1]]*len(s),files[ann_fil][1:9])

            # Step 3. Apply the functions to the segments, then store the features in the db

            # MEAN
            mean = create_feature_from_segment(t,np.mean)
            add_feature_to_db(user_loc,hands[j],'mean_' + signals + '_' + components[comp],mean,files[ann_fil][1:9])

            # STD
            std = create_feature_from_segment(t, np.std)
            add_feature_to_db(user_loc, hands[j], 'std_' + signals + '_' + components[comp], std,files[ann_fil][1:9])

            # PEAKS
            nmpeaks = create_feature_from_segment(t,EDA_features_extraction.peak_detection)
            add_feature_to_db(user_loc, hands[j], 'num_peaks_' + signals + '_' + components[comp], nmpeaks,files[ann_fil][1:9])

            peakamp = create_feature_from_segment(t,EDA_features_extraction.peak_amplitude)
            add_feature_to_db(user_loc, hands[j], 'amp_peaks_' + signals + '_' + components[comp], peakamp,files[ann_fil][1:9])

            # MIN, MAX, DIFF
            min = create_feature_from_segment(t, np.amin)
            add_feature_to_db(user_loc, hands[j], 'min_' + signals + '_' + components[comp], min,files[ann_fil][1:9])

            max = create_feature_from_segment(t, np.amax)
            add_feature_to_db(user_loc, hands[j], 'max_' + signals + '_' + components[comp], max, files[ann_fil][1:9])

            diff = create_feature_from_segment(t, EDA_features_extraction.difference)
            add_feature_to_db(user_loc, hands[j], 'diff_' + signals + '_' + components[comp],diff , files[ann_fil][1:9])

            # SLOPE COMPUTED WITH LINEAR REGRESSION
            slope = create_feature_from_segment(t, EDA_features_extraction.signal_slope)
            add_feature_to_db(user_loc, hands[j], 'slope_' + signals + '_' + components[comp],slope , files[ann_fil][1:9])
            print "SLOPE"
            print slope

    # Concat together the baseline, laughter databases of all the user in a final db called new
    hands = ['left']
    new = pd.DataFrame()
    old = pd.DataFrame()
    for h in range(0, len(hands)):
     for u in range(0, len(user)):

          db_laugh = pd.read_csv(dir + user[u]  + hands[h] +'_laughter_Database.csv')
          db_base = pd.read_csv(dir + user[u]  + hands[h] + '_baseline_Database.csv')
          db_laugh_base = pd.concat([db_laugh,db_base])
          new = pd.concat([old,db_laugh_base])
          old = new

          print new
          new.to_csv(dir + 'EDA_' +  hands[h] +'_additional_all.csv',index=0)