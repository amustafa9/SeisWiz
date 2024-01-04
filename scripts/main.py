import argparse
from seismic_slicer import SeismicSlicer


def main():
    # # Create ArgumentParser object
    # parser = argparse.ArgumentParser(description='Program running RegressNet Horizon Tracker')
    #
    # # Add optional argument
    # parser.add_argument('-i', '--input_file', required=True, help='Path to the configuration file')
    # parser.add_argument('-f', '--fast_scan', required=True, help='Set to True if fast scanning of segy file is desired')
    #
    # # Parse the command line arguments
    # args = parser.parse_args()

    seismic_slicer = SeismicSlicer(r"E:\seismic_volumes_python\input_cubes\169394_11.lto.RTM_enhanced_stack_OBN_TTI.6586761042_input.segy",
                                   horizon_file_path=r"E:\seismic_volumes_python\result_compare")

    # seismic_slicer = SeismicSlicer(r"E:\seismic_volumes_python\input_cubes\169394_11.lto.RTM_enhanced_stack_OBN_TTI.6586761042_input.segy")


if __name__ == "__main__":
    main()