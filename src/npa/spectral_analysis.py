import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import src.npa.filters as filters
from src.npa.utils import *

<<<<<<< HEAD
def psd(data, channels, time_range = None,fpass = [0.1, 150.0], plot_on = True, save_fig = None):
=======
from neurodsp.sim import sim_combined
from neurodsp.plts import plot_time_series, plot_timefrequency
from neurodsp.utils import create_times

# Import function for Morlet Wavelets
from neurodsp.timefrequency.wavelets import compute_wavelet_transform
from neurodsp.spectral import compute_spectrum, rotate_powerlaw
def psd(data, channels, fpass = [0.1, 150.0], plot_on = True, save_fig = None):
>>>>>>> c6a091a113ae81f1e9ae290e1223bc999bc5385d
    '''
    Returns and plots power spectral density for selected channels using welches method
    :param data:
    :param channels:
    :param time_range: time range in seconds [0,X]
    :param fpass:
    :param plot_on:
    :return:
    '''
    fs = data.metadata['sample_rate']
    type = data.metadata['stream_name']
    num_channels = data.metadata['num_channels']
    ds_factor = 10 # factor by which to downsample data
    data_ = convert_samples(data) # convert data to voltage
    chan_pxx = list()
    dfs = fs / ds_factor  # set downsampled rate
    if time_range == None:
        time_range=[0,-1]
        data_ = data_[:,:]
    else:
        time_range = [int(time_range[0]*fs),int(time_range[1]*fs)]
        data_ = data_[time_range[0]:time_range[1],:]
    print(data_.shape)
    win = 4 * dfs
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
        if len(channels) > 1:
            fig, ax = plt.subplots(nrows=len(channels))
            for i,chan in enumerate(channels):
                ax[i].semilogy(f,chan_pxx[chan], color = 'black', linewidth = 2)
                ax[i].set_title('Channel {} Power Spectral Density'.format(chan+1))
                ax[i].set_ylabel('PSD [V**2/Hz]')
                ax[i].set_xlabel('Frequency (Hz)')
        else:
            fig, ax = plt.subplots()
            ax.semilogy(f,chan_pxx[channels[0]],color = 'black', linewidth = 2)
            ax.set_title('Channel {} Power Spectral Density'.format(channels[0] + 1))
            ax.set_ylabel('PSD [V**2/Hz]')
            ax.set_xlabel('Frequency (Hz)')
        if save_fig != None:
            plt.savefig(save_fig+'_NP_PSD.png')
        plt.show()
    return f, chan_pxx

def spectrogram(data, channels, time_range = None, fpass = [0.1, 150.0]):
    fs = data.metadata['sample_rate']
    type = data.metadata['stream_name']
    num_channels = data.metadata['num_channels']
    win = 4 * fs
    ds_factor = 10  # factor by which to downsample data
    data_ = convert_samples(data)  # convert data to voltage
    if time_range == None:
        time_range=[0,-1]
        data_ = data_[:,:]
    else:
        time_range = [int(time_range[0]*fs),int(time_range[1]*fs)]
        data_ = data_[time_range[0]:time_range[1],:]
    chan_pxx = list()
    dfs = fs / ds_factor  # set downsampled rate
    for chan in channels:
        b, a = filters.notch(fs)
        filt_data = signal.filtfilt(b, a, data_[:, chan])
        # bandpass filter
        b, a = filters.bandpass(fs, [fpass[0], fpass[1]])
        filt_data = signal.filtfilt(b, a, filt_data)

        # downsample data
        filt_data = signal.decimate(filt_data, ds_factor)

        f, t, sxx = signal.spectrogram(filt_data, dfs, nperseg=1024) #, nperseg = ) # use pcolormesh
    return f, t, sxx

def welch_spectrum(data, channel, fpass = [0.1, 150.0]):
    fs = data.metadata['sample_rate'] # get sampling rate
    channels = convert_samples(data) # convert to microvolts
    chan = channels[:,channel] # get channel data vector
    # filter data
    b, a = filters.notch(fs)
    filt_data = signal.filtfilt(b, a, chan)
    b, a = filters.bandpass(fs, [fpass[0], fpass[1]])
    filt_data = signal.filtfilt(b, a, filt_data)

    freq_mean, psd_mean = compute_spectrum(filt_data, fs, method='welch', avg_type='mean', nperseg=fs*2)
    return freq_mean, psd_mean
def morlet_wavelet(data, channel, fpass = [0.1, 150.0],freq_vec=[5,100,50], n_cycles=7, plot_fig=True):
    fs = data.metadata['sample_rate'] # get sampling rate
    channels = convert_samples(data) # convert to microvolts
    chan = channels[:,channel] # get channel data vector
    # filter data
    b, a = filters.notch(fs)
    filt_data = signal.filtfilt(b, a, chan)
    b, a = filters.bandpass(fs, [fpass[0], fpass[1]])
    filt_data = signal.filtfilt(b, a, filt_data)

    freqs = np.linspace(freq_vec[0],freq_vec[1],freq_vec[2]) # set frequency vector
    ts = np.linspace(0,len(filt_data)/fs,len(filt_data))
    mwt = compute_wavelet_transform(filt_data,fs=fs,n_cycles=n_cycles, freqs=freqs)
    return freqs, ts, mwt, filt_data

