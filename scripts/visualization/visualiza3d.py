from seismic_canvas import (SeismicCanvas, volume_slices, XYZAxis, Colorbar)
from vispy import app
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, Colormap


def visualize_3d_vispy(seismic_array, horizon_vol=None, x_slice=0, y_slice=0, z_slice=0):
    """opens an interactive window to visualize the given 3d numpy array"""

    # clip seismic
    seismic_array = np.clip(seismic_array, -5, 5)

    # set up slicing
    slicing = {'x_pos': x_slice, 'y_pos': y_slice, 'z_pos': z_slice}

    if horizon_vol is not None:
        z_coords, y_coords, x_coords = np.where(horizon_vol==1)
        seismic_array[z_coords, y_coords, x_coords] = 6

    # set up canvas
    visual_nodes = volume_slices([seismic_array],
                                  cmaps=["gray"],
                                  clims=[(-5, 6)],
                                  # The preprocessing functions can perform some simple gaining ops.
                                  preproc_funcs=[None],
                                  interpolation='bilinear', **slicing)

    # define canvas parameters
    canvas_params = {'size': (2560, 1377),
                     'axis_scales': (1, 1, 1.5),  # stretch z-axis
                     'colorbar_region_ratio': 0.1,
                     'fov': 30, 'elevation': 39, 'azimuth': 43,
                     'zoom_factor': 1}

    # define axes
    xyz_axis = XYZAxis(seismic_coord_system=True)

    canvas = SeismicCanvas(title='Seismic',
                            visual_nodes=visual_nodes,
                            xyz_axis=xyz_axis,
                            **canvas_params)

    app.run()