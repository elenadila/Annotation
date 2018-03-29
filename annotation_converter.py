import pandas as pd
from datetime import timedelta
import datetime
import time
from os.path import basename
import os
import math

"""
    Methods for the conversion of the timestamp from the ANVIL timestamps
"""


# Convert the annotation table got from ANVIL into a DataFrame
def annotation_conversion(filename):
  df = pd.read_csv(filename,delimiter="\t")
  return df

# Look whether in a folder there is a video and if it is, return the filename without extension,
# This corresponds to the beginning of the video expressed as: ddmmyyhhmmss
def video_name_converter(dir):
 for subdir, dirs, files in os.walk(dir):
     for file in files:
     #   print file
        if (file.endswith(".MP4")):
            os.path.splitext(file)
            filename = os.path.splitext(file)[0]
 return filename


# Convert the filename expressed as: ddmmyyhhmmss into a time stamp in the format: yy-mm-dd hh:mm:ss
def filename_converter(dir_path):
 file_name = video_name_converter(dir_path)
 day = file_name[0:2]
 month = file_name[2:4]
 year = file_name[4:8]
 hour = file_name[8:10]
 minutes = file_name[10:12]
 seconds = file_name[12:14]
 experiment_day = datetime.datetime(int(year),int(month),int(day), int(hour), int(minutes),int(seconds))

 return experiment_day

# Create an annotaion db with additional columns: start_converted and end_converted.
# start_converted: experiment_day + seconds when the laughter started in yy-mm-dd hh:mm:ss format
# end_converted: experiment_day + seconds when the laughter ended in yy-mm-dd hh:mm:ss
def annotation_time_converter(directory, filepath):
    db = annotation_conversion(filepath)
    day_ex = filename_converter(directory)
    dur = (db['duration'])
    print dur
    print day_ex
    start = db['start'].values
    end = db['end'].values
    start_converted = []
    end_converted = []
    duration_converted = []
    for i in range(0, len(start)):
        # Round the timestamp to the nearest second
        start_converted.append(pd.Timestamp((day_ex + timedelta(seconds=start[i]))).round('1s'))
        end_converted.append(pd.Timestamp(day_ex + timedelta(seconds=end[i])).round('1s'))
        duration_converted.append((end_converted[i]-start_converted[i]).total_seconds())
    print duration_converted
    db['start_converted'] = start_converted
    db['end_converted'] = end_converted
    db['duration_converted'] = duration_converted
    # Add to the file a timestamp corresponding to the beg of the segm + 5 seconds
    db['end_converted_5_sec'] = (pd.to_datetime(start_converted) + timedelta(seconds=5))

    db.to_csv(filepath, sep="\t", index=0)

    return db




if __name__ == '__main__':
    dir = "C:\Users\user\Desktop\Pilot_Study/"
    file = 'baseline_additional_removed.txt'
    dir = "C:\Users\user\Desktop\Pilot_Study/"
    signals = ['EDA', 'BVP', 'HR', 'TEMP', 'ACC', 'IBI']
    user = ['u001/', 'u002/', 'u003/', 'u004/', 'u005/', 'u008/']
    for participant in range(0, len(user)):
        db_ann = pd.read_csv(dir + user[participant] + file,delimiter="\t")
        start_converted = db_ann['start_converted']
        db_ann['end_converted_5_sec'] = (pd.to_datetime(start_converted) + timedelta(seconds=5))
        db_ann.to_csv(dir + user[participant] + file, sep="\t", index=0)

