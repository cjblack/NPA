import matplotlib.pyplot as plt
import utils


def plot_channels(data, channels, fontsize=8, layout='compressed'):
    '''
    Basic plotting for data channels
    :param data:
    :param channels:
    :param fontsize:
    :param layout:
    :return:
    '''
    metadata = data.metadata
    fs = metadata['sample_rate']
    timestamps = data.sample_numbers/fs
    timestamps = timestamps - timestamps[0]
    data = utils.convert_samples(data)
    fig, ax = plt.subplots(nrows=len(channels), figsize = (5,10), layout=layout)
    for chan in channels:
        ax[chan].plot(timestamps,data[:,chan], color = 'black')
        ax[chan].set_title('Chan {}'.format(chan+1), fontsize=fontsize)
        ax[chan].set_ylabel('uV', fontsize=fontsize)
        ax[chan].set_xlabel('Time (s)', fontsize=fontsize)
    fig.tight_layout()
    plt.show()