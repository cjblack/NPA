from open_ephys.analysis import Session

def load_data(directory, node_idx: int = 0, rec_idx: int = 0):
    '''
    Returns all continuous data for specific recording
    :param directory: str, directory of the recorded data
    :param node_idx: int, index of record node to access
    :param rec_idx: int, index of recording to access
    :return:
    '''
    session = Session(directory)
    continuous = session.recordnodes[node_idx].recordings[rec_idx].continuous
    return continuous

def get_spike_data(directory, node_idx: int = 0, rec_idx: int = 0):
    '''
    Returns action potential data and metadata
    :param directory:
    :param node_idx:
    :param rec_idx:
    :return:
    '''
    continuous = load_data(directory, node_idx = node_idx, rec_idx = rec_idx)
    return continuous[0]

def get_lfp_data(directory, node_idx: int = 0, rec_idx: int = 0):
    '''
    Returns LFP data and metadata
    :param directory:
    :param node_idx:
    :param rec_idx:
    :return:
    '''
    continuous = load_data(directory, node_idx = node_idx, rec_idx = rec_idx)
    return continuous[1]

def convert_samples(data):
    data = data.get_samples(start_sample_index = 0, end_sample_index = data.samples.shape[0])
    return data
