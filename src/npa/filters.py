import numpy as np
from scipy import signal

def notch(fs, f0: float = 50.0, Q: float = 30.0):
    b, a = signal.iirnotch(f0,Q,fs)
    return b, a

def bandpass(fs, fband, order: int = 2):
    b, a = signal.butter(order, [fband[0], fband[1]], fs = fs, btype='band')
    return b, a

def notch_filter_data(data, fs):
    b, a = notch(fs)
    fdata = signal.filtfilt(b, a, data)
    return fdata

def bandpass_filter_data(data, fs, fpass):
    b, a = bandpass(fs, fpass)
    fdata = signal.filtfilt(b, a, data)
    return fdata