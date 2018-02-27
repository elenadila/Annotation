import pandas as pd
import segmentation
import matplotlib.pyplot as plt


def plot_laughter(dir, user, hand, signal,annotation):
    signal_name = signal
    df_laughter = pd.read_csv(dir + user +
                              annotation, delimiter="\t")
    start = pd.to_datetime(df_laughter.start_converted.values)
    end = pd.to_datetime(df_laughter.end_converted.values)

    df_signal = pd.read_csv(dir + user+ hand + '/' + signal + '_Table.csv')
    laugher_id = df_laughter.ID.values

    for i in range (0,len(start)):
        trace = segmentation.part_div(df_signal[signal],df_signal.Time,start[i],end[i])
        trace.plot()
        plt.title(user + '_' + signal_name + '_' + hand + '_' + laugher_id[i] )
        plt.savefig(dir + user + 'graphs/' + signal + '/' + hand + '_' + laugher_id[i] + '.png')
      #  plt.show()
        plt.close()



if __name__ == '__main__':
    dir = "C:\Users\user\Desktop\Pilot_Study/"
    user = 'u001/'

    signals = ['IBI']
    # signals = ['ACC']
    hands = ['right', 'left']

    laughter_annotation_file = '/laughter_annotation.txt'


    for p in range(0, len(signals)):
        for j in range(0, len(hands)):
            plot_laughter(dir, user, hands[j], signals[p],laughter_annotation_file)