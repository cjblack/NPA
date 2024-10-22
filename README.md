# NPA
Neuropixel Analysis tools

## To-do
* Add comments to plotting
* Filter for electrodes based on signal property

## Setup
### open ephys tools
Follow from https://github.com/open-ephys/open-ephys-python-tools

1. Create a new anaconda environment
```
conda env create -n NPA
conda activate NPA
```
2. Install Open Ephys python tools

`
$ pip install open-ephys-python-tools
`

## Usage
### Loading data
```
directory = 'location/of/neuropix/data'

from src.npa.utils import *

# getting lfp data
lfp = get_lfp_data(directory)
lfp_samples = lfp.samples
lfp_metadata = lfp.metadata

# getting action potential data
ap = get_spike_data(directory)
ap_samples = ap.samples
ap_metadata = ap.metadata
```

### Plotting frequency response
```
directory = 'location/of/neuropix/data' # set directory of neuropixel data
from src.npa.utils import *
from src.npa.plots import *

lfp = get_lfp_data(directory) # load data
plot_probe_freq(lfp, probe_region=[0,75]) #  plots first 76 electrodes

```
