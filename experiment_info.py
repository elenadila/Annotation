import pandas as pd
from datetime import timedelta
from annotation_converter import filename_converter
from database_creation import check_create_db
import time
import pymysql

# Read from the mysql db the registration_information table which contains the users' info anf the begininning and end of
# the experiment
def add_info_to_db(dir_path,username, event_name, event_start, event_duration):
    # check if the experiment_info file exists, if yes read it, otherwise create it.
    db = check_create_db(dir_path + username, "experiment_info.csv")
    # Connect to the mysql db and store the table in a pandas dataframe: registration_info
    connection = pymysql.connect(host='localhost', port=3306, user='root', password='', db='registration')
    registration_info = pd.read_sql('SELECT * FROM registration_information', connection)
    registration_info.to_csv(dir_path + 'registration_information_all_users.csv')
    # Store in the experiment_info the beg, end and duration of the particular stimulus
    db['type'] = [event_name]
    beg = (pd.to_datetime(registration_info[registration_info['user_id']==username[0:4]].start_timestamp) + timedelta(seconds=event_start))
    beg = beg.iloc[0]
    db['start'] = beg
    db['end'] = (pd.to_datetime(beg) + timedelta(seconds=event_duration))
    db['duration'] = event_duration
    return db

# Create a experiment_info file with all the stimuli information
def reconstruct_video_info(dir, user):
    baseline_1 = add_info_to_db(dir, user,"baseline_1",4,60)
    video_1 = add_info_to_db(dir, user,"cat_falling",65,40)
    video_2 = add_info_to_db(dir, user, "baby",107,48)
    video_3 = add_info_to_db(dir, user, "guy",157,29)
    video_4 = add_info_to_db(dir, user, "giraffe",188,22)
    video_5 = add_info_to_db(dir, user, "babies",212,163)
    video_6 = add_info_to_db(dir, user, "crazy_cat",377,33)
    video_7 = add_info_to_db(dir, user, "movies",412,227)
    video_8 = add_info_to_db(dir, user, "people_falling",641,95)
    clapping = add_info_to_db(dir, user, "clapping",739,9)
    cognitive = add_info_to_db(dir, user, "cognitive_load",751,30)
    baseline_2 = add_info_to_db(dir, user, "baseline_2",787,60)
    experiment = add_info_to_db(dir, user, "experiment",0,852)

    db_info = pd.concat([baseline_1,video_1,video_2,video_3,video_4,video_5,video_6,video_7,video_8,
                         clapping,cognitive,baseline_2,experiment])
    del db_info['random']
    db_info.to_csv(dir + user + "experiment_info.csv", index=0)


if __name__ == '__main__':
    dir = "C:\Users\user\Desktop\Pilot_Study/"
    user = ['u001/', 'u002/', 'u003/', 'u004/', 'u005/', 'u006/']

    for i in range(0,len(user)):
       # Create an empty experiment_info file for each user
       datab = pd.DataFrame({'random': []})
       datab.to_csv(dir + user[i] + "experiment_info.csv", index=0)
       reconstruct_video_info(dir,user[i])
