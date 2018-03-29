import numpy as np
import pandas as pd
import scipy.signal as scisig
import os
import matplotlib.pyplot as plt

def windowing(data,fun,window_size,stride):
    result_wind = [fun(data[i:i+window_size]) for i in range(0, len(data), stride)
                   if i+window_size < len(data) ]
    return result_wind



def acc_moving_avg(dir,user, hand):
    acc_table = pd.read_csv(dir + user + hand + "ACC_Table.csv")
    x_component = acc_table['0'].values
    y_component = acc_table['1'].values
    z_component = acc_table['2'].values





DEBUG = True

SAMPLING_RATE = 32

ONE_MINUTE_S = 60
THIRTY_MIN_S = ONE_MINUTE_S * 30
SECONDS_IN_DAY = 24 * 60 * 60

STILLNESS_MOTION_THRESHOLD = .1
PERCENT_STILLNESS_THRESHOLD = .95

STEP_DIFFERENCE_THRESHOLD = 0.3


# Motion signal: root mean squared 3 axis acceleration
def computeMotion(acc1, acc2, acc3):
    '''Aggregates 3-axis accelerometer signal into a single motion signal'''
    return np.sqrt(np.array(acc1) ** 2 + np.array(acc2) ** 2 + np.array(acc3) ** 2)


def filterSignalFIR(eda, cutoff=0.4, numtaps=64):
	f = cutoff/(SAMPLING_RATE/2.0)
	FIR_coeff = scisig.firwin(numtaps,f)

	return scisig.lfilter(FIR_coeff,1,eda)


def countStillness(stillness):
    '''Counts the total percentage of time spent still over a period
    Args:
        stillness:	an binary array at 1Hz that is 1 if that second is part of a still period
    Returns:
        the percentage time spent still over a period'''

    return float(sum(stillness)) / float(len(stillness))


def aggregateSignal(signal, new_signal_length, agg_method='sum'):
    new_signal = np.zeros(new_signal_length)
    samples_per_bucket = len(signal) / new_signal_length

    # the new signal length must be large enough that there is at least 1 sample per bucket
    assert (samples_per_bucket > 0)

    for i in range(new_signal_length):
        if agg_method == 'sum':
            new_signal[i] = np.nansum(signal[i * samples_per_bucket:(i + 1) * samples_per_bucket])
        elif agg_method == 'percent':
            new_signal[i] = np.nansum(signal[i * samples_per_bucket:(i + 1) * samples_per_bucket]) / samples_per_bucket
        elif agg_method == 'mean':
            new_signal[i] = np.nanmean(signal[i * samples_per_bucket:(i + 1) * samples_per_bucket])
        elif agg_method == 'max':
            new_signal[i] = np.nanmax(signal[i * samples_per_bucket:(i + 1) * samples_per_bucket])
    return new_signal


def getIndexFromTimestamp(hours, mins=0):
    return ((hours * 60) + mins) * 60 * SAMPLING_RATE






if __name__ == "__main__":

    dir = "C:\Users\user\Desktop\Pilot_Study/"
    #user = ['u001/', 'u002/', 'u003/', 'u004/', 'u005/', 'u006/']
    user = ['u008/']
    hands = ['right', 'left']

    for participant in range(0,len(user)):
            for j in range(0, len(hands)):
                acc = pd.read_csv(dir + user[participant] + hands[j] + '/ACC_Table.csv')
                acc_comp = computeMotion(acc['0'], acc['1'], acc['2'])
                acc['ACC'] = acc_comp
                filtered_signal = filterSignalFIR(acc_comp)
                diff = filtered_signal[1:] - filtered_signal[:-1]

                acc['ACC_Filtered'] = filtered_signal
             #   acc.append(pd.DataFrame({'Diff':diff}))
                acc.to_csv(dir + user[participant] + hands[j] + '/ACC_Table.csv', index=0)

              #  plt.plot(acc_comp)
             #   plt.show()