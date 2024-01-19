import argparse
from seismic_slicer import SeismicSlicer


def main():
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description='Program running RegressNet Horizon Tracker')

    # Add arguments
    parser.add_argument('-i', '--input_file', required=True, help='Path to the input segy file')
    parser.add_argument('-hor', '--horizon_path', required=False, help='Path to a specific horizon picks file or a directory containing multiple horizon files')
    parser.add_argument('-cmap', '--color_map', required=False, help='Colormap to render the seismic data. Must be a matplotlib compatible.')
    parser.add_argument('-att', '--attribute_volume_file', required=False, help='Path to an attribute segy file that needs be overlaid on the original seismic')

    # Parse the command line arguments
    args = parser.parse_args()

    # extract values of the arguments
    path_segy = args.input_file  # path to segy file

    # construct keyword argument dictionary to handle optional arguments
    keyword_dict = {'horizon_file_path': args.horizon_path,
                    'cmap': args.color_map,
                    'att': args.attribute_volume_file}

    # initialize seismic slicer with the user-supplied arguments
    seismic_slicer = SeismicSlicer(path_segy=path_segy, **keyword_dict)


if __name__ == "__main__":
    main()
