import matplotlib.pyplot as plt
from src.npa.utils import *
import numpy as np
import src.npa.spectral_analysis as spec
import src.npa.filters as filters

def plot_channels_separate(data, channels, fontsize=8, layout='compressed'):
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
    data = convert_samples(data)
    fig, ax = plt.subplots(nrows=len(channels), figsize = (5,10), layout=layout)
    for i, chan in enumerate(channels):
        ax[i].plot(timestamps,data[:,chan], color = 'black')
        ax[i].set_title('Chan {}'.format(chan+1), fontsize=fontsize)
        ax[i].set_ylabel('uV', fontsize=fontsize)
        ax[i].set_xlabel('Time (s)', fontsize=fontsize)
    fig.tight_layout()
    plt.show()

def plot_channels_together(data, channels, v_factor=100):
    metadata = data.metadata
    fs = metadata['sample_rate']
    timestamps = data.sample_numbers/fs
    timestamps = timestamps - timestamps[0]
    data = convert_samples(data)
    n = len(channels)
    colors = plt.cm.plasma(np.linspace(0,1,n))
    for i, chan in enumerate(channels):
        sig = data[:,chan]
        fsig = filters.notch_filter_data(sig, fs)
        fsig = filters.bandpass_filter_data(fsig, fs, fpass=[0.1, 150.0])
        plt.plot(timestamps, fsig+(chan*v_factor), color=colors[i])
    plt.xlabel('Time (s)')
    plt.show()

def plot_channels_epoch(data, channels, event_time, v_factor = 100):
    """
    Plot channels with respect to event time...
    :param data: lfp data
    :param channels: range of channels to plot in list
    :param event_time: time in seconds of when 'event' occured
    :param v_factor: scaling factor for plotting channels on same axis
    :return:
    Use:
    >>>plot_channels_epoch(lfp,range(0,100),4.5)
    """
    metadata = data.metadata
    fs = metadata['sample_rate']
    timestamps = data.sample_numbers/fs
    timestamps = timestamps - timestamps[0]
    event_idx = np.where((abs(timestamps-event_time))==np.min(abs(timestamps-event_time)))
    tpre = event_idx[0]-fs # 1 second pre
    tpost = event_idx[0]+fs # 1 secont post
    data = convert_samples(data)
    n = len(channels)
    colors = plt.cm.plasma(np.linspace(0,1,n))
    for i, chan in enumerate(channels):
        sig = data[:,chan]
        fsig = filters.notch_filter_data(sig, fs)
        fsig = filters.bandpass_filter_data(fsig, fs, fpass=[0.1, 150.0])
        plt.plot(timestamps[int(tpre):int(tpost)], fsig[int(tpre):int(tpost)]+(chan*v_factor), color=colors[i])
    plt.xlabel('Time (s)')
    plt.show()

def plot_power_spectra(data, channel, save_dir=None):
    """
    Plots power spectral density using the welch method
    :param data: open ephys lfp data object
    :param channel: channel index to plot
    :param save_dir: directory to save data in string format if desired
    :return:
    Use:
    For not saving figure...
    >>>plot_power_spectra(lfp,0)
    For saving figure...
    >>>plot_power_spectra(lfp,0,save_dir='location/to/save/file')
    """
    name = data.name.split('/')[0]
    type = name.split('-')[-1]
    if type != 'LFP':
        raise TypeError('Use only LFP data types.')
    f, pxx = spec.welch_spectrum(data, channel)
    plt.plot(f,pxx)
    plt.xlim([0,100])
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('PSD (uV^2/Hz)')
    plt.title('Channel {} PSD'.format(channel+1))
    if save_dir != None:
        plt.savefig(save_dir+'/'+'channel_{}_psd.pdf'.format(channel+1))
    plt.show()
def plot_spectrogram(data, channel, x_ticks=5, y_ticks=5):
    """
    Plots spectrogram of LFP and filtered LFP trace using morlet wavelet
    :param data:
    :param channel:
    :param x_ticks:
    :param y_ticks:
    :return: t, f, mwt: time (t) and frequency (f) vectors, as well as morlet wavelet transform (mwt)
    Use:
    >>> t, f, mwt = plot_spectrogram(lfp, 0)
    """
    # Partially adapted from neurodsp
    # first check that this is LFP data:
    name = data.name.split('/')[0]
    type = name.split('-')[-1]
    if type != 'LFP':
        raise TypeError('Use only LFP data types.')
    f, t, mwt, sig = spec.morlet_wavelet(data,channel)
    if np.iscomplexobj(mwt):
        powers = abs(mwt)
    fig, ax = plt.subplots(nrows=2, layout='compressed')
    pos = ax[0].imshow(powers,aspect='auto')
    ax[0].invert_yaxis()
    ax[0].set_xlabel('Time (s)')
    ax[0].set_ylabel('Frequency (Hz)')
    fig.colorbar(pos, ax = ax[0])
    if isinstance(x_ticks, int):
        x_tick_pos = np.linspace(0, t.size, x_ticks)
        x_ticks = np.round(np.linspace(t[0], t[-1], x_ticks), 2)
    else:
        x_tick_pos = [np.argmin(np.abs(t - val)) for val in x_ticks]
        ax[0].set(xticks=x_tick_pos, xticklabels=x_ticks)
    ax[0].set(xticks=x_tick_pos, xticklabels=x_ticks)

    if isinstance(y_ticks, int):
        y_ticks_pos = np.linspace(0, f.size, y_ticks)
        y_ticks = np.round(np.linspace(f[0], f[-1], y_ticks), 2)
    else:
        y_ticks_pos = [np.argmin(np.abs(f - val)) for val in y_ticks]
        ax[0].set(yticks=y_ticks_pos, yticklabels=y_ticks)
    ax[0].set(yticks=y_ticks_pos, yticklabels=y_ticks)

    ax[1].plot(t,sig)
    ax[1].set_xlabel('Time (s)')
    ax[1].set_ylabel('Voltage (uV)')
    fig.suptitle('Channel {} Spectrogram'.format(channel+1))
    plt.show()

    return t, f, mwt
def plot_probe_rms(data, probe='1_3A', probe_region=None):
    '''
    Plots rms voltage across each electrode position
    :param data:
    :param probe:
    :return:
    '''
    metadata = data.metadata
    data = convert_samples(data)
    channels = data.shape[1]
    rms = np.zeros((channels,1))

    # get channel mapping
    chan_loc = get_channel_locs(probe)
    chan_map = get_channel_map(probe)

    # calculate Vrms
    for chan in range(channels):
        rms[chan] = np.sqrt(np.mean(data[:,chan]**2))
    #rms_norm = rms/np.max(rms) # normalize for coloring
    rms_ = rms[chan_map].reshape((187,2))
    fig, ax = plt.subplots()
    cmap = plt.colormaps['plasma']
    im = ax.pcolormesh(rms_,cmap=cmap)
    ax.set_aspect(0.1)
    ax.set_title('Probe voltage')
    ax.set_xlabel('X position (um)')
    ax.set_ylabel('Y position (um)')
    fig.colorbar(im)
    if probe_region != None:
        ax.set_ylim([probe_region[0],probe_region[1]])
    plt.show()

def plot_probe_freq(data, probe='1_3A', freq_range=[80.0,100.0], probe_region=None, save_fig=None):
    '''
    Plots total power in specified frequency band across probe
    :param data: open ephys structure
    :param probe: neuropixel probe version being used
    :param freq_range: range of frequencies to analyze [float,float]
    :param probe_region: area of probe to plot [int, int]
    :return:
    '''
    channels = list(range(384))
    pxx_mean = np.zeros((len(channels)))
    f,pxx = spec.psd(data,channels,plot_on=False) # keep plotting off to avoid a nightmare
    freq_idxs = np.where(np.logical_and(f>=freq_range[0],f<freq_range[1]))

    # get channel mapping
    chan_loc = get_channel_locs(probe)
    chan_map = get_channel_map(probe)

    for chan in channels:
        pxx_ = pxx[chan]/np.max(pxx[chan])
        pxx_mean[chan] = np.sum(pxx_[freq_idxs])

    pxx_mean_ = pxx_mean[chan_map].reshape((187,2))
    fig, ax = plt.subplots()
    cmap = plt.colormaps['plasma']
    if probe_region != None:
        im = ax.pcolormesh(pxx_mean_[probe_region[0]:probe_region[1],:],cmap=cmap)
    else:
        im = ax.pcolormesh(pxx_mean_, cmap=cmap)
    ax.set_aspect(0.1)
    ax.set_title('Probe total power {}Hz:{}Hz'.format(str(freq_range[0]),str(freq_range[1])))
    ax.set_xlabel('X position (um)')
    ax.set_ylabel('Y position (um)')
    fig.colorbar(im)
    if probe_region != None:
        ax.set_ylim([probe_region[0],probe_region[1]])
    if save_fig != None:
        plt.savefig(save_fig+'_NP'+probe+'-probe_freq.png')
    plt.show()