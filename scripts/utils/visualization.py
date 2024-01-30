import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from pathlib import Path


def plot_section_slices(array, x_pos, y_pos):
    """function returns an image consisting of stitched slices in il and xl directions for seismic volume array"""
    h1, w1 = array[0].T.shape  # height and width of orthogonal slices along first axis
    _, w2 = array[:,0,:].T.shape  # height and width of orthogonal slices along second axis

    image_stitched = np.zeros((h1, w1+w2))
    image_stitched[:,:y_pos] = array[x_pos,:y_pos].T
    image_stitched[:, y_pos:y_pos+w2-x_pos] = array[x_pos:,y_pos,:].T
    return image_stitched


def plot_depth_slice(array, z_pos):
    """function returns depth slice from seismic volume array at z_pos"""
    return array[:,:,z_pos]


def extract_section_picks(sorted_unique_inlines, sorted_unique_xlines, samples, inline_picks, xline_picks, z_picks,
                          current_inline_num, current_xline_num):
    """function returns indices of horizon picks to plot on stitched inline/crossline view of the 2D slicer

    Parameters
    ----------
    sorted_unique_inlines: array
        array of all unique inlines in the segy seismic file sorted in ascending order
    sorted_unique_xlines: array
        array of all unique xlines in the segy seismic file sorted in ascending order
    inline_picks: array
        array of inline picks in horizon
    xline_picks: array
        array of xline picks in horizon
    z_picks: array
        array of time/depth picks

    Returns
    -------
    sorted_x_coords: array
        array of x-axis coords to plot on section view
    sorted_y_coords: array
        array of y-axis coords to plot on section view
    """

    # generate mask of valid picks to plot on seismic
    mask_valid = (inline_picks >= sorted_unique_inlines.min()) & (inline_picks <= sorted_unique_inlines.max()) & \
                 (xline_picks >= sorted_unique_xlines.min()) & (xline_picks <= sorted_unique_xlines.max()) & \
                 (z_picks < samples.max())

    # filter out picks not contained within survey geometry
    inline_picks = inline_picks[mask_valid]
    xline_picks = xline_picks[mask_valid]
    z_picks = z_picks[mask_valid]

    # digitize picks along inline and crossline
    ilines_digitized = np.digitize(inline_picks, bins=sorted_unique_inlines)
    xlines_digitized = np.digitize(xline_picks, bins=sorted_unique_xlines)

    # create arrays to store x and y coordinates of picks
    x_coords = []  # to store x positions of horizon picks
    y_coords = []  # to store y positions of horizon picks

    # subsample picks for current inline
    mask_valid = (ilines_digitized == current_inline_num)

    # add inline section picks
    for x_pick, y_pick in zip(xlines_digitized[mask_valid].tolist(), z_picks[mask_valid].tolist()):
        if x_pick < current_xline_num:
            x_coords.append(x_pick)
            y_coords.append(y_pick)
        else:
            pass

    # subsample picks for current xline
    mask_valid = (xlines_digitized == current_xline_num)

    # add xline section picks to x_coords
    for x_pick, y_pick in zip(ilines_digitized[mask_valid].tolist(), z_picks[mask_valid].tolist()):
        if x_pick > current_inline_num:
            x_coords.append(x_pick - current_inline_num + current_xline_num)
            y_coords.append(y_pick)
        else:
            pass

    # convert lists to numpy arrays
    x_coords = np.array(x_coords, dtype=int)
    y_coords = np.array(y_coords, dtype=int)

    # sort by x values
    sorting_inds_x = np.argsort(x_coords)
    sorted_x_coords = x_coords[sorting_inds_x]
    sorted_y_coords = y_coords[sorting_inds_x]

    return sorted_x_coords, sorted_y_coords



def create_section_sliders(nil, nxl, nz, init_vals=(0,0,0)):
    """function creates three slider objects to allow user to interactively change inline, crossline, and
    depth slice positions in the volume

    Parameters:
        nil: int
            number of inlines in the volume
        nxl: int
            number of crosslines in the volume
        nz: int
            number of time/depth samples in the volume
        init_vals: tuple of int
            tuple specifying the initial frame values along inline, crossline, and depth directions
        """

    # Add slider for interactive frame navigation along inline direction
    axframe1 = plt.axes([0.1, 0.01, 0.5, 0.03], facecolor='lightgoldenrodyellow')
    frame_slider1 = Slider(axframe1, 'Inline Num', 0, nil - 1, valinit=init_vals[0], valstep=1)

    # Add slider for interactive frame navigation along crossline direction
    axframe2 = plt.axes([0.1, 0.06, 0.5, 0.03], facecolor='lightgoldenrodyellow')
    frame_slider2 = Slider(axframe2, 'Xline Num', 0, nxl - 1, valinit=init_vals[1], valstep=1)

    # Add slider for interactive frame navigation along time/depth direction
    axframe3 = plt.axes([0.1, 0.11, 0.5, 0.03], facecolor='lightgoldenrodyellow')
    frame_slider3 = Slider(axframe3, 'Depth Slice Num', 0, nz - 1, valinit=init_vals[2], valstep=1)

    return frame_slider1, frame_slider2, frame_slider3


def create_clip_slider():
    """function creates and returns a slider object to manipulate the clipping applied to the seismic images in terms
    of its standard deviation"""

    clip_axis = plt.axes([0.7, 0.06, 0.25, 0.03], facecolor='lightgoldenrodyellow')
    clip_slider = Slider(clip_axis, 'Clip', 1, 10, valinit=3, valstep=1)

    return clip_slider


def create_threshold_slider(min, max):
    """function creates and returns a slider object to perform thresholding on attribute volume"""

    thresh_axis = plt.axes([0.7, 0.01, 0.25, 0.03], facecolor='lightgoldenrodyellow')
    attr_range = np.linspace(min, max, 10)
    threshold_slider = Slider(thresh_axis, 'Threshold', min, max, valinit=attr_range[4], valstep=attr_range[1] - attr_range[0])

    return threshold_slider


def list_files_in_directory(directory_path):
    path_obj = Path(directory_path)

    # Use a list comprehension to filter out only files
    files = [str(file) for file in path_obj.iterdir() if file.is_file()]

    return files


def rescale(arr):
    arr_min = arr.min()
    arr_max = arr.max()
    return (arr - arr_min) / (arr_max - arr_min)


def threshold(arr, thresh, min, max):
    arr_threshold = arr.copy()
    mask = arr_threshold<=thresh
    arr_threshold[mask] = min
    arr_threshold[~mask] = max
    return arr_threshold
