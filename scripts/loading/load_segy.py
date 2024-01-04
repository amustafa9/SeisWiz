# Script contains function to convert segy formatted seismic volumes to numpy arrays for processing and visualization
# in Python

import segyio
import numpy as np


def segy2npy(segy_path, fast_scan=True, **kwargs):
    """function takes an unstructured segy file and creates a numpy array corresponding to the 3D seismic volume

    Args:
        segy_path (string): path to segy file

    Returns:
        numpy_vol (array): 3D numpy array of the form crosslines x inlines x samples representing the seismic volume
        xlines (array): array of sorted unique xline numbers in the segy file
        ilines (array): array of sorted unique inline numbers in the segy file
        samples (array): array of time/depth samples in segy file
    """

    # read segy file
    segy_file = segyio.open(segy_path, ignore_geometry=True)

    # get a list of all crosslines in the file
    if fast_scan:
        all_xlines = np.array([segy_file.header[i][segyio.TraceField.CROSSLINE_3D] for i in range(0,segy_file.tracecount,10)])
    else:
        all_xlines = np.array([segy_file.header[i][segyio.TraceField.CROSSLINE_3D] for i in range(0, segy_file.tracecount)])

    unique_xlines = np.sort(np.unique(all_xlines)).astype(int)

    # get a list of all inlines in the file
    if fast_scan:
        all_ilines = np.array([segy_file.header[i][segyio.TraceField.INLINE_3D] for i in range(0,segy_file.tracecount,10)])
    else:
        all_ilines = np.array([segy_file.header[i][segyio.TraceField.INLINE_3D] for i in range(0, segy_file.tracecount)])

    unique_ilines = np.sort(np.unique(all_ilines)).astype(int)

    # array of depth\time samples
    samples = np.sort(segy_file.samples)

    # create numpy array to store seismic volume
    seismic_cube = np.zeros((unique_ilines.size, unique_xlines.size, samples.size))

    print("Parsing Segy File...")
    for i in range(segy_file.tracecount):
        # find relative inline position for trace
        absolute_xline = int(segy_file.header[i][segyio.TraceField.CROSSLINE_3D])
        relative_xline = np.where(unique_xlines==absolute_xline)[0].item()

        # find relative crossline position for trace
        absolute_iline = int(segy_file.header[i][segyio.TraceField.INLINE_3D])
        relative_iline = np.where(unique_ilines==absolute_iline)[0].item()

        seismic_cube[relative_iline, relative_xline] = segy_file.trace[i]

    print("Segy parsing completed!")

    # obtain volume cut outs
    if kwargs['min_iline'] is not None:
        min_il_idx = np.digitize(kwargs['min_iline'], np.sort(unique_ilines))
        seismic_cube = seismic_cube[min_il_idx:,:,:]
        unique_ilines = unique_ilines[min_il_idx:]

    if kwargs['max_iline'] is not None:
        max_il_idx = np.digitize(kwargs['max_iline'], np.sort(unique_ilines))
        seismic_cube = seismic_cube[:max_il_idx+1, :, :]
        unique_ilines = unique_ilines[:max_il_idx+1]

    if kwargs['min_xline'] is not None:
        min_xl_idx = np.digitize(kwargs['min_xline'], np.sort(unique_xlines))
        seismic_cube = seismic_cube[:, min_xl_idx:, :]
        unique_xlines = unique_xlines[min_xl_idx:]

    if kwargs['max_xline'] is not None:
        max_xl_idx = np.digitize(kwargs['max_xline'], np.sort(unique_xlines))
        seismic_cube = seismic_cube[:, :max_xl_idx+1, :]
        unique_xlines = unique_xlines[:max_xl_idx + 1]

    if kwargs['min_time'] is not None:
        min_time_idx = np.digitize(kwargs['min_time'], np.sort(samples))
        seismic_cube = seismic_cube[:, :, min_time_idx:]
        samples = samples[min_time_idx:]

    if kwargs['max_time'] is not None:
        max_time_idx = np.digitize(kwargs['max_time'], np.sort(samples))
        seismic_cube = seismic_cube[:, :, :max_time_idx+1]
        samples = samples[:max_time_idx+1]

    return seismic_cube, unique_ilines, unique_xlines, samples