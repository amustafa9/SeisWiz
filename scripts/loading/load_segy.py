# Script contains function to convert segy formatted seismic volumes to numpy arrays for processing and visualization
# in Python

import segyio
import numpy as np


def get_segy_crosslines(segy_file, skip):
    """function returns a list of crosslines for each trace in the provided segy_file using the skip option provided"""
    return np.array([segy_file.header[i][segyio.TraceField.CROSSLINE_3D] for i in range(0,segy_file.tracecount,skip)])


def get_segy_inlines(segy_file, skip):
    """function returns a list of inlines for each trace in the provided segy_file using the skip option provided"""
    return np.array([segy_file.header[i][segyio.TraceField.INLINE_3D] for i in range(0,segy_file.tracecount,skip)])

def create_cube_from_segy(segy_file, unique_ilines, unique_xlines, samples):
    """function creates a 3D numpy array containing the seismic cube from the segy file and the list of sorted
    inlines, crosslines, and depth/time samples"""

    # create numpy array to store seismic volume
    seismic_cube = np.zeros((unique_ilines.size, unique_xlines.size, samples.size))

    # read each trace and put into the appropriate position in the cube
    for i in range(segy_file.tracecount):
        # find relative inline position for trace
        absolute_xline = int(segy_file.header[i][segyio.TraceField.CROSSLINE_3D])
        relative_xline = np.where(unique_xlines == absolute_xline)[0].item()

        # find relative crossline position for trace
        absolute_iline = int(segy_file.header[i][segyio.TraceField.INLINE_3D])
        relative_iline = np.where(unique_ilines == absolute_iline)[0].item()

        seismic_cube[relative_iline, relative_xline] = segy_file.trace[i]

    return seismic_cube


def segy2npy(segy_path):
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
    all_xlines = get_segy_crosslines(segy_file, skip=20)
    unique_xlines = np.sort(np.unique(all_xlines)).astype(int)

    # get a list of all inlines in the file
    all_ilines = get_segy_inlines(segy_file, skip=20)
    unique_ilines = np.sort(np.unique(all_ilines)).astype(int)

    # array of depth\time samples
    samples = np.sort(segy_file.samples)

    try:
        print("Parsing Segy File...")
        seismic_cube = create_cube_from_segy(segy_file, unique_ilines, unique_xlines, samples)
        print("Segy parsing completed!")

    except ValueError:
        print("Missed inlines and/or crosslines on the first pass. Re-reading segy file with every trace...")

        # get crosslines
        all_xlines = get_segy_crosslines(segy_file, skip=1)
        unique_xlines = np.sort(np.unique(all_xlines)).astype(int)

        # get inlines
        all_ilines = get_segy_inlines(segy_file, skip=1)
        unique_ilines = np.sort(np.unique(all_ilines)).astype(int)

        # recreate cube with re-parsed inline/crossline information
        seismic_cube = create_cube_from_segy(segy_file, unique_ilines, unique_xlines, samples)
        print("Segy parsing completed!")

    return seismic_cube, unique_ilines, unique_xlines, samples