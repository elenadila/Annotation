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

    for i in range(len(sig)):
        normalized.append(((sig[i] - np.mean(sig)) / (max_val - min_val)))
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


if __name__ == '__main__':
    dir = "C:\Users\user\Desktop\Pilot_Study/"
    user = 'u003/'

    signals = 'EDA_Table.csv'
    # signals = ['ACC']

    hands = ['right/', 'left/']

    for j in range(0, len(hands)):
            db = pandas.read_csv(dir + user + hands[j] + signals)

            [r, p, t, l, d, e, obj] = decomposition(db.EDA, 4)
            db['Phasic'] = r
            db['Tonic'] = t
            db.to_csv(dir + user + hands[j] + signals, index=0)
