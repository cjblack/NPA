import matplotlib.pyplot as plt
from npa.utils import *
import numpy as np
import spectral_analysis as spec

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
    data = convert_samples(data)
    fig, ax = plt.subplots(nrows=len(channels), figsize = (5,10), layout=layout)
    for chan in channels:
        ax[chan].plot(timestamps,data[:,chan], color = 'black')
        ax[chan].set_title('Chan {}'.format(chan+1), fontsize=fontsize)
        ax[chan].set_ylabel('uV', fontsize=fontsize)
        ax[chan].set_xlabel('Time (s)', fontsize=fontsize)
    fig.tight_layout()
    plt.show()

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
    :param data:
    :param probe:
    :param freq_range:
    :param probe_region:
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