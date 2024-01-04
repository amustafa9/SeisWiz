import argparse
from seismic_slicer import SeismicSlicer


def main():
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description='Program running RegressNet Horizon Tracker')

    # Add arguments
    parser.add_argument('-i', '--input_file', required=True, help='Path to the configuration file')
    parser.add_argument('-hor', '--horizon_path', required=False, help='Path to a specific horizon picks file or a directory containing multiple horizon files')
    parser.add_argument('-f', '--fast_scan', required=False, help='Set to True if fast scanning of segy file is desired')

    # Parse the command line arguments
    args = parser.parse_args()

    # extract values of the arguments
    path_segy = args.input_file  # path to segy file

    # construct keyword argument dictionary
    keyword_dict = {'horizon_file_path': args.horizon_path}

    # initialize seismic slicer with the user-supplied arguments
    seismic_slicer = SeismicSlicer(path_segy=path_segy, fast_scan=True, **keyword_dict)


if __name__ == "__main__":
    main()