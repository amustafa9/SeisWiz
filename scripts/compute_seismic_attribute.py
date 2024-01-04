import numpy as np
import matplotlib.pyplot as plt
from loading.load_segy import *
from processing.dip2d import *

# load seismic
data_path = r"E:\seismic_volumes_python\input_cubes\169394_11.lto.RTM_enhanced_stack_OBN_TTI.6586761042_input.segy"
seismic, _, _, _ = segy2npy(data_path, fast_scan=True, min_iline=None, max_iline=None, min_xline=None, max_xline=None,
                            min_time=None, max_time=None)

# extract a random inline section
section = seismic[300, 800:1000, 200:400].T

# compute dip
dip_section = dip2d(section, niter=20)

# display
fig, ax = plt.subplots()
ax.imshow(section, vmin=-3*section.std(), vmax=3*section.std(), cmap='gray')
ax.imshow(dip_section.squeeze(), alpha=0.5, cmap='bwr')
plt.show()


