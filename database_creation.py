import pandas as pd
import numpy as np
import segmentation
import os

# Segments the signal based on start and end of the laughter episode
def segment_episodes(dir, user, hand, signal,annotation):

    signal_name = signal
    # Read the laughter annotation file and store the start,end and duration of the episodes
    df_laughter = pd.read_csv(dir + user +
                              annotation, delimiter="\t")
    start = pd.to_datetime(df_laughter.start_converted.values)
    end = pd.to_datetime(df_laughter.end_converted.values)
    df_signal = pd.read_csv(dir + user+ hand + '/' + signal + '_Table.csv')
    laugher_id = df_laughter.ID.values
    duration = df_laughter.duration
    traces =[]
    # Segments the signal in traces
    for i in range (0,len(start)):
        trace = segmentation.part_div(df_signal[signal],df_signal.Time,start[i],end[i])
        traces.append(trace)

    return (traces, start, end, laugher_id,duration)

# Applies the desired function fun to the segment and returns the feature
def function_to_apply(segment, fun):
    if segment.empty:
        print "empty"
        feature = np.NaN
       # print feature
    else:
        feature = fun(segment)
    return feature

# Creates a feature array applying the function_to_apply to all the segments
def create_feature_from_segment(segment_traces, function):
    feat_column = []
    for i in range(0,len(segment_traces)):
        feat_column.append(function_to_apply(segment_traces[i],function))
    print feat_column
    return feat_column


# Add the feature_array to the database
def add_feature_to_db(user_dir,hand, feature_name, feature_column,signal_name):
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
            datab = pd.DataFrame({'user_id':[]})
            datab.to_csv(filename, index=0)
            datab = pd.read_csv(filename)
            print 'not-found'
 return datab



if __name__ == '__main__':
    dir = "C:\Users\user\Desktop\Pilot_Study/"
    user = 'u001/'
    signals = ['EDA', 'BVP', 'HR', 'TEMP', 'ACC', 'IBI']
    hands = ['right','left']
    laughter_annotation_file = '/laughter_annotation.txt'
    user_loc = dir + user


    # Step 1. Divide the signal in segments: segment_episodes
    # Step 2. Add the feature column to the database - first the generic: start, end, laughter id, user id
    # Step 3. Apply the functions to the segments, then store the features in the db

    for p in range(0, len(signals)):
        for j in range(0, len(hands)):
            [t, s, e ,id, d] = segment_episodes(dir, user, hands[j], signals[p], laughter_annotation_file)
            print t
            print t
            print np.mean(d)
            add_feature_to_db(user_loc, hands[j], 'start', s,'Laughter')
            add_feature_to_db(user_loc, hands[j], 'end', e,'Laughter')
            add_feature_to_db(user_loc, hands[j], 'laugter_id', id,'Laughter')
            add_feature_to_db(user_loc, hands[j],'duration', d,'Laughter')
            add_feature_to_db(user_loc, hands[j],'hand', hands[j],'Laughter')
            add_feature_to_db(user_loc, hands[j], 'user_ID', [user[0:len(user)-1]]*len(s),'Laughter')
            add_feature_to_db(user_loc, hands[j], 'type', ['laughter'] * len(s),'Laughter')
            mean = create_feature_from_segment(t,np.mean,)
            add_feature_to_db(user_loc,hands[j],'mean_' + signals[p],mean,'Laughter')
            std = create_feature_from_segment(t, np.std)
            add_feature_to_db(user_loc, hands[j], 'std_' + signals[p], std,'Laughter')





