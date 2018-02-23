import pandas
import numpy as np
import matplotlib.pyplot as plt
#import cvxEDA
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


def signal_extraction(path):
    signal = [];

    with open(path, 'rt') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')

        for row in spamreader:
            signal.append(', '.join(row))
    return signal


def time_extraction(signal, signal_name):
    i = 0;
    time = [];
    sample_rate = 0
    if signal_name == 'EDA':
        sample_rate = 4.0
    if signal_name == 'TEMP':
        sample_rate = 4.0
    if signal_name == 'BVP':
        sample_rate = 64.0
    if signal_name == 'HR':
        sample_rate = 1.0

    if signal_name == 'ACC':
        sample_rate = 32.0

    for i in range(len(signal)):
        print signal[0]
        time.append(datetime.fromtimestamp(float(signal[0])) + timedelta(minutes=float((i/sample_rate)/60)))  #the time is expressed in minutes
    return time

def signal_time_table(dir, user, hand, signal_name ):
    table_name = signal_name + '_' + 'Table.csv'

    if signal_name == 'ACC':
        acc = pandas.read_csv(dir + user + hand + '/' + signal_name + '.csv', header=None)
        time_raw = time_extraction(acc.iloc[:,0], signal_name)
        acc = acc.drop(acc.index[0:2])
        df = pandas.DataFrame(acc)
        del time_raw[len(time_raw) - 1]
        del time_raw[len(time_raw) - 1]
        df['Time'] = time_raw
        df.to_csv(dir + user + hand + '/' + table_name, index=0)
    else:

     signal_raw = signal_extraction(dir + user + hand + '/' + signal_name + '.csv')

     time_raw = time_extraction(signal_raw, signal_name)
     del signal_raw[0:2]  # I am deleting the first row from EDA values because is the first TIMESTAMP
     del time_raw[len(time_raw) - 1]
     del time_raw[len(time_raw) - 1]


     df = pandas.DataFrame({'Raw': signal_raw, 'Time': time_raw})

     df.to_csv(dir + user + hand + '/' + table_name, index=0)


if __name__ == '__main__':
    dir = "C:\Users\user\Desktop\Pilot_Study/"
    user = 'u001/'

    #signals = ['EDA', 'BVP', 'HR', 'TEMP','ACC']
    signals = ['ACC']

    hands = ['right','left']
    for p in range(0,len(signals)):
        for j in range(0,len(hands)):
            signal_time_table(dir,user,hands[j],signals[p])



