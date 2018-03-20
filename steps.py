import segmentation
import signals_table_creation
import annotation_converter
import database_creation
import experiment_info
import baseline_segmentation
import pandas as pd
if __name__ == '__main__':

    dir = "C:\Users\user\Desktop\Pilot_Study/"
    signals = ['EDA', 'BVP', 'HR', 'TEMP', 'ACC', 'IBI']
    user = ['u001/', 'u002/', 'u003/', 'u004/', 'u005/', 'u006/']
    hands = ['right', 'left']
    annotation_files = ['laughter_annotation.txt','additional_annotation.txt']
#------------------------------------------------------------------------------------------------------------------------------------------#

    """ Step 1: Extract the experiment informarions and create a file with start, end, duration of each stimulus """

    # for i in range(0, len(user)):
        #  datab = pd.DataFrame({'random': []})
         # datab.to_csv(dir + user[i] + "experiment_info.csv", index=0)
    #     experiment_info.reconstruct_video_info(dir, user[i])

#-----------------------------------------------------------------------------------------------------------------------------------------#
    """ Step 2: Create the table for each signal """

    for participant in range(0,len(user)):
      for p in range(0, len(signals)):
            for j in range(0, len(hands)):
                signals_table_creation.signal_time_table(dir, user[participant], hands[j], signals[p])

#-----------------------------------------------------------------------------------------------------------------------------------------#

    """ Step 3: Convert the timestamps from the annotation file from ANVIL to a useful format """

    for participant in range(0,len(user)):
      for file in range(0, len(annotation_files)):

            annotation_converter.annotation_time_converter(dir, dir + user[participant] + annotation_files[file])

#------------------------------------------------------------------------------------------------------------------------------------------#

    """ Step 4: apply the pre-processing procedure to all the signals"""
    # TODO

# ------------------------------------------------------------------------------------------------------------------------------------------#

    """ Step 5: segment the signals into laughter episodes and create the database """
    # TODO: in database_creation.py

# ------------------------------------------------------------------------------------------------------------------------------------------#

    """ Step 6: segment the baseline and compute features from it """
    #TODO

# ------------------------------------------------------------------------------------------------------------------------------------------#

    """ Step 7: combine the databases of all particiapants in a single db and compute statistics """

    #TODO






