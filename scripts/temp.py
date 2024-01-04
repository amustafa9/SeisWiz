# imports
from loading.load_segy import segy2npy
from visualization.slicer_utils import *
import matplotlib.pyplot as plt


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
            x_coords.append(x_pick+current_xline_num)
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


il = 399
xl = 1000
# read seismic
path_segy = r"E:\seismic_volumes_python\input_cubes\169394_11.lto.RTM_enhanced_stack_OBN_TTI.6586761042_input.segy"
seismic, ilines, xlines, samples = segy2npy(path_segy, fast_scan=True, min_iline=None, max_iline=None,
                                                    min_xline=None, max_xline=None, min_time=None, max_time=None)

# extract seismic parameters
seismic = seismic
ilines = np.sort(ilines)
xlines = np.sort(xlines)
samples = np.sort(samples)
std = seismic.std()

# extract horizon
horizon_file_path = r"E:\seismic_volumes_python\horizons_ilxl\MM7_P2_C_DD.txt"
horizon_file = np.genfromtxt(horizon_file_path)

# extract horizon picks
inline_picks = horizon_file[1:, 0].astype(int)
xline_picks = horizon_file[1:, 1].astype(int)
z_picks = horizon_file[1:, 2].astype(int)

# extract x/y picks to plot on section view
x_coords, y_coords = extract_section_picks(np.sort(ilines), np.sort(xlines), np.sort(samples),
                                           inline_picks, xline_picks, z_picks, il, xl)

# show stitch image
img = plot_section_slices(seismic, il, xl)

plt.imshow(img, cmap='gray', vmin=-3*std, vmax=3*std,
           extent=(0, seismic.shape[0]+seismic.shape[1], samples.max(), samples.min()), aspect='auto')

plt.plot(x_coords, y_coords)
plt.show()

