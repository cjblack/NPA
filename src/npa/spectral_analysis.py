from scipy import signal
import matplotlib.pyplot as plt
import filters
import utils

def psd(data, channels, fpass = [0.1, 150.0], plot_on = True):
    '''
    Returns and plots power spectral density for selected channels using welches method
    :param data:
    :param channels:
    :param fpass:
    :param plot_on:
    :return:
    '''
    fs = data.metadata['sample_rate']
    type = data.metadata['stream_name']
    num_channels = data.metadata['num_channels']
    win = 4*fs
    ds_factor = 10 # factor by which to downsample data
    data_ = utils.convert_samples(data) # convert data to voltage
    chan_pxx = list()
    dfs = fs / ds_factor  # set downsampled rate
    # notch filter
    for chan in channels:
        b, a = filters.notch(fs)
        filt_data = signal.filtfilt(b, a, data_[:, chan])
        # bandpass filter
        b, a = filters.bandpass(fs, [fpass[0], fpass[1]])
        filt_data = signal.filtfilt(b, a, filt_data)

        # downsample data
        filt_data = signal.decimate(filt_data, ds_factor)

        f, pxx = signal.welch(filt_data, dfs, nperseg = win)
        chan_pxx.append(pxx)
    if plot_on:
        fig, ax = plt.subplots(nrows=len(channels))
        for chan in channels:
            ax[chan].semilogy(f,chan_pxx[chan], color = 'black', linewidth = 2)
            ax[chan].set_title('Channel {} Power Spectral Density'.format(chan+1))
            ax[chan].set_ylabel('PSD [V**2/Hz]')
            ax[chan].set_xlabel('Frequency (Hz)')
        plt.show()
    return f, chan_pxx