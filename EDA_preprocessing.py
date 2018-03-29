import pandas
import numpy as np
import matplotlib.pyplot as plt
import cvxEDA
import pylab as pl
import scipy as sp
from scipy import signal
import csv
from datetime import *
from datetime import timedelta
import pandas
from pandas import DataFrame # In order to write into the .csv file we can use the pandas module
import os
import matplotlib.pyplot as plt
import scipy.signal as scisig
import pandas as pd
from segmentation import part_div



# This function extracts EDA values from the csv file.
# The input of the function is the path of the file.
def eda_extraction(str):
    eda = [];

    with open(str, 'rt') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')

        for row in spamreader:
            eda.append(', '.join(row))
    return eda

# This function generates the time for each EDA value based on the first timestamp and the sampling rate.
# First timestamp is the first row in EDA.csv file
# Sampling rate is the second row in EDA.csv file
def time_extraction(eda):
    i = 0;
    time = [];
    for i in range(len(eda)):
        time.append(datetime.fromtimestamp(float(eda[0])) + timedelta(minutes=float((i/4.0)/60)))  #the time is expressed in minutes
    return time

# Signal normalization between 0 and 1
def normalization(sig):
    sig = map(lambda x: float(x), sig)
    sig = list(sig)
    normalized = []
    min_val = min(sig)
    max_val = max(sig)

    for i in range(0,len(sig)):

        normalized.append(((sig[i] - min_val) / (max_val - min_val)))
    #normalized.append(np.mean(normalized))
    return normalized

def decomposition(eda, Fs):
    y = np.array((eda))
    yn = (y - y.mean()) / y.std()
    [r, p, t, l, d, e, obj] = cvxEDA.cvxEDA(yn, 1./Fs)
    return (np.array(a).ravel() for a in (r, p, t, l, d, e, obj))

def filtering(eda, window):
    filtered = sp.signal.medfilt(eda, window)
    return filtered


def windowing(data,fun,window_size,stride):
    result_wind = [fun(data[i:i+window_size]) for i in range(0, len(data), stride)
                   if i+window_size < len(data) ]
    return result_wind
#To filter the noise using the Bartlett filter with a win_size size of the window
    # win_size is the frequency of sensor values
def filtering_bartlett(sig, win_size):
    win = signal.bartlett(win_size)
    win = map(lambda x: float(x),win)
    sig = map(lambda x: float(x),sig)
    win = list(win)
    sig = list(sig)

    filtered = signal.convolve(sig, win, mode='same') / sum(win)
    return filtered

def butter_lowpass(cutoff, fs, order=5):
    # Filtering Helper functions
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = scisig.butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    # Filtering Helper functions
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = scisig.lfilter(b, a, data)
    return y

if __name__ == '__main__':
    dir = "C:\Users\user\Desktop\Pilot_Study/"
    user = ['u001/', 'u002/', 'u003/', 'u004/', 'u005/', 'u006/','u008/']
 #   user = ['u008/']
    signals = 'EDA_Table.csv'
    output = 'EDA_Table_Experiment.csv'


    hands = ['right/', 'left/']
    for participant in range(0,len(user)):
      for j in range(0, len(hands)):
            eda_table = pandas.read_csv(dir + user[participant] + hands[j] + signals)

            filename = dir + user[participant] + 'experiment_info.csv'
            df_info = pd.read_csv(filename)
            start = pd.to_datetime(df_info[df_info['type'] == 'experiment'].start)
           # end = pd.to_datetime(df_info[df_info['type'] == 'experiment'].end)
            end = pd.to_datetime(df_info.end_from_registration)


            start = start.iloc[0]
            end = end.iloc[0]

            eda_experiment = part_div(eda_table, eda_table.Time, start, end)

            print user[participant], hands[j]
            filtered = butter_lowpass_filter(eda_experiment['EDA'], 1.0, 8, 6)
            eda_experiment['EDA_Filtered'] = filtered
            [r, p, t, l, d, e, obj] = decomposition(eda_experiment.EDA, 4)
            eda_experiment['Phasic'] = normalization(r)
            eda_experiment['Tonic'] = normalization(t)
            eda_experiment['Normalized'] = normalization(filtered)

            eda_experiment.to_csv(dir + user[participant] + hands[j] + output, index=0)
