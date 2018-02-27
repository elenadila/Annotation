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
   # i = 0
    time = []

    print "signal"
    print signal
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


    for cont in range(0,len(signal)):
         time.append(datetime.fromtimestamp(float(signal[0])) + timedelta(minutes=float((cont/sample_rate)/60)))  #the time is expressed in minutes

    return time

def signal_time_table(dir, user, hand, signal_name ):
    table_name = signal_name + '_' + 'Table.csv'
    acc = pandas.DataFrame()
    if signal_name == 'ACC':
        acc = pandas.read_csv(dir + user + hand + '/' + signal_name + '.csv', header=None)
        time_raw = time_extraction(acc.iloc[:,0], signal_name)
        acc = acc.drop(acc.index[0:2])
        df = pandas.DataFrame(acc)
        del time_raw[len(time_raw) - 1]
        del time_raw[len(time_raw) - 1]

        df['Time'] = time_raw
        acc_mean = []
        avg = []
        for i in range(0,len(time_raw)-1):
            acc_mean.append(max(np.abs(df.iloc[i,0] - df.iloc[i-1,0]),
                                    np.abs((df.iloc[i,1] - df.iloc[i-1,1])),
                                   np.abs(df.iloc[i,2] - df.iloc[i-1,2])))
            mean = np.mean([df.iloc[i,0],df.iloc[i,1],df.iloc[i,2]])
            avg.append(mean* 0.9 + (acc_mean[i] / 32) * 0.1)

        acc_mean.append(0)



        df['ACC'] = acc_mean
        df.to_csv(dir + user + hand + '/' + table_name, index=0)

    elif signal_name == 'IBI':
        ibi = pandas.read_csv(dir + user + hand + '/' + signal_name + '.csv', header=None)
        time_raw = ibi.iloc[:,0]
        time = []
        initial_timestamp = datetime.fromtimestamp(float(time_raw[0]))
        for i in range(0, len(time_raw)):
            time.append((initial_timestamp + timedelta(seconds=time_raw[i])).strftime("%Y-%m-%d %H:%M:%S"))
        df_ibi = pandas.DataFrame({'IBI':ibi.iloc[:,1], 'Time':time})
        df_ibi = df_ibi.drop(df_ibi.index[0:2])
        df_ibi.to_csv(dir + user + hand + '/' + table_name, index=0)




    else:

     signal_raw = signal_extraction(dir + user + hand + '/' + signal_name + '.csv')

     time_raw = time_extraction(signal_raw, signal_name)
     del signal_raw[0:2]  # I am deleting the first row from EDA values because is the first TIMESTAMP
     del time_raw[len(time_raw) - 1]
     del time_raw[len(time_raw) - 1]


     df = pandas.DataFrame({signal_name: signal_raw, 'Time': time_raw})

     df.to_csv(dir + user + hand + '/' + table_name, index=0)


if __name__ == '__main__':
    dir = "C:\Users\user\Desktop\Pilot_Study/"
    user = 'u001/'

    signals = ['EDA', 'BVP', 'HR', 'TEMP','ACC','IBI']
   # signals = ['ACC']

    hands = ['right','left']
    for p in range(0,len(signals)):
        for j in range(0,len(hands)):
            signal_time_table(dir,user,hands[j],signals[p])



