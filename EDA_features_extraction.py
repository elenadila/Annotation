from EDA_preprocessing import *
import Peak_detection
from scipy import stats

def peak_detection(signal):
    indices = Peak_detection.indexes(signal, thres=0.01, min_dist=4)
    x = indices
    y = [signal[t] for t in indices]
    numpeak = len(y)

    # Average Amplitude of peaks
    avpeak = np.mean(y)

    return numpeak


def peak_amplitude(signal):
    indices = Peak_detection.indexes(signal, thres=0.01, min_dist=4)
    x = indices
    y = [signal[t] for t in indices]
    numpeak = len(y)

    # Average Amplitude of peaks
    avpeak = np.mean(y)

    return avpeak


# the dynamic range (DRSC), defined as the difference between Max and Min -
# from: Electrodermal Activity Sensor for Classification of Calm/Distress Condition
def difference(signal):

    diff = np.amax(signal) - np.amin(signal)
    print "DIFF"
    print np.amax(signal), np.amin(signal), diff
    return  diff


# Slope extimated from linear regression
# (similar to Using Electrodermal Activity to Recognize Ease of Engagement in Children during Social Interactions Javier)
def signal_slope(signal):
    # create an array of coordinates from 0 to the len of the signal,to provide to the linregress
    x_coord = np.arange(0,len(signal))

    slope, intercept, r_value, p_value, std_err = stats.linregress(x_coord, signal)

    return slope