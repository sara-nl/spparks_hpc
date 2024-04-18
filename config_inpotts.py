"""
Last modified on 18 Apr 2024

Script that for a given new case_name (ex: 'vHpdV_20_0_20_LL_x_10_60_30_7_40_75_35_12_0_1'):
    - check if the corresponding folder already exists
    - if not exists, create folder with case_name as name 
    - copy init files to case_name folder
    - amend in.potts (update values of parameters in it)

This script is executed on-the-fly every time a new line is read from the config_file.
        
"""

import shutil
import os
from argparse import ArgumentParser
from typing import List, Tuple
import numpy as np


def folder_exists(working_dir: str, config_name: str) -> bool:
    folder_exists: bool = False

    for root, dirs, files in os.walk(working_dir):
        for name in dirs:
            if name.endswith(config_name):
                folder_exists = True
                break
        break

    return folder_exists


def create_folder(working_dir, config_name):
    directory = os.path.join(working_dir, config_name)
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError as e:
        print("Error: Creating directory. " + directory)
        raise e
    return directory


def copy_initial_condition(working_dir, directory, init_file="IN100_3d.init"):

    # Construct full paths to the source and destination files
    src = os.path.join(working_dir, init_file)
    dst = os.path.join(directory, init_file)

    try:
        # Ensure the destination directory exists; create if it does not
        os.makedirs(directory, exist_ok=True)

        # Copy the file from source to destination
        shutil.copyfile(src, dst)
    except FileNotFoundError:
        print(
            f"Error: The source file {src} does not exist or the destination cannot be found."
        )
    except PermissionError:
        print(f"Error: Permission denied when accessing {src} or {directory}.")
    except OSError as os_error:
        print(f"Error: {os_error}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def create_config_map(config_str: str) -> tuple:
    # Remove the 'vHpdV_' prefix
    values = config_str.split("_")[1:]

    # Convert the individual values
    v1 = float(values[0] + "." + values[1])
    v2 = int(values[2])
    v3 = values[3]
    v4 = values[4]

    # Convert the values to a list of integers except for the last two values
    HAZ_list = [int(val) for val in values[5:-2]]
    HAZ_list.append(float(values[-2] + "." + values[-1]))

    return (v1, v2, v3, v4, HAZ_list)


def amend_spparks_file(case_name, working_dir, input_file="in.potts_am_IN100_3d"):
    """
    Create config map from case name string
    """
    config_map = create_config_map(case_name)

    src_file = os.path.join(working_dir, input_file)
    case_dir = os.path.join(working_dir, case_name)
    dst_file = os.path.join(case_dir, input_file)

    if not os.path.isfile(src_file):
        raise FileNotFoundError(f"The source file {src_file} does not exist.")

    # open files from template & copy new file in the case directory
    with open(
        src_file,
        "r",
    ) as template, open(dst_file, "a") as new_spparks_file:
        # calculate single hatch line coordinates
        V_x = config_map[0]
        V_y = config_map[0]
        hatch_x = config_map[1]
        hatch_y = config_map[1]
        ATOI = config_map[4]
        # ATOI = [int(i) for i in ATOI_str[0:8]]
        # ATOI.append(float(ATOI_str[8:9]))

        if config_map[3] == "x":
            if config_map[2] == "LL":
                LAYER = "am cartesian_layer 1 start LL pass_id 1 thickness 25 offset -100.0 0.0"
            if config_map[2] == "UL":
                LAYER = "am cartesian_layer 1 start UL pass_id 1 thickness 25 offset 100.0 0.0"
            if config_map[2] == "LR":
                LAYER = "am cartesian_layer 1 start LR pass_id 1 thickness 25 offset -100.0 0.0"
            if config_map[2] == "UR":
                LAYER = "am cartesian_layer 1 start UR pass_id 1 thickness 25 offset 100.0 0.0"
        elif config_map[3] == "y":
            if config_map[2] == "LL":
                LAYER = "am cartesian_layer 1 start LL pass_id 1 thickness 25 offset 0.0 -100.0"
            if config_map[2] == "UL":
                LAYER = "am cartesian_layer 1 start UL pass_id 1 thickness 25 offset 0.0 100.0"
            if config_map[2] == "LR":
                LAYER = "am cartesian_layer 1 start LR pass_id 1 thickness 25 offset 0.0 -100.0"
            if config_map[2] == "UR":
                LAYER = "am cartesian_layer 1 start UR pass_id 1 thickness 25 offset 0.0 100.0"

        # open file corresponding to the selected file name & write coordinates
        # in new structure according to template
        # read content from first file
        for num, line in enumerate(template):
            # append content to second file
            if num <= 10:
                new_spparks_file.write(line)
            elif num > 10 and num <= 11:
                new_spparks_file.write("variable V_x equal " + str(V_x) + "\n")
            elif num > 11 and num <= 12:
                new_spparks_file.write("variable V_y equal " + str(V_y) + "\n")
            elif num > 12 and num <= 14:
                new_spparks_file.write(line)
            elif num > 14 and num <= 15:
                new_spparks_file.write("variable HATCH_x equal " + str(hatch_x) + "\n")
            elif num > 15 and num <= 16:
                new_spparks_file.write("variable HATCH_y equal " + str(hatch_y) + "\n")
            elif num > 16 and num <= 24:
                new_spparks_file.write(line)
            elif num > 24 and num <= 25:
                new_spparks_file.write(
                    "variable case_name universe " + case_name + "\n"
                )
            elif num > 25 and num <= 30:
                new_spparks_file.write(line)
            elif num > 30 and num <= 31:
                new_spparks_file.write("variable ATOI_1 equal " + str(ATOI[0]) + "\n")
            elif num > 31 and num <= 32:
                new_spparks_file.write("variable ATOI_2 equal " + str(ATOI[1]) + "\n")
            elif num > 32 and num <= 33:
                new_spparks_file.write("variable ATOI_3 equal " + str(ATOI[2]) + "\n")
            elif num > 33 and num <= 34:
                new_spparks_file.write("variable ATOI_4 equal " + str(ATOI[3]) + "\n")
            elif num > 34 and num <= 35:
                new_spparks_file.write("variable ATOI_5 equal " + str(ATOI[4]) + "\n")
            elif num > 35 and num <= 36:
                new_spparks_file.write("variable ATOI_6 equal " + str(ATOI[5]) + "\n")
            elif num > 36 and num <= 37:
                new_spparks_file.write("variable ATOI_7 equal " + str(ATOI[6]) + "\n")
            elif num > 37 and num <= 38:
                new_spparks_file.write("variable ATOI_8 equal " + str(ATOI[7]) + "\n")
            elif num > 38 and num <= 39:
                new_spparks_file.write("variable ATOI_9 equal " + str(ATOI[8]) + "\n")
            elif num > 39 and num <= 93:
                new_spparks_file.write(line)
            elif num > 93 and num <= 94:
                new_spparks_file.write(LAYER + "\n")
            elif num > 94 and num <= 97:
                new_spparks_file.write(line)
            else:
                new_spparks_file.write(line)


def main(args):
    working_dir = args.working_dir
    case_name = args.case_name

    if not folder_exists(working_dir, case_name):
        case_directory = create_folder(working_dir, case_name)
        copy_initial_condition(working_dir, case_directory)
        amend_spparks_file(case_name, working_dir)


if __name__ == "__main__":
    parser = ArgumentParser()
    home_dir = os.environ["HOME"]
    parser.add_argument(
        "--working_dir",
        type=str,
        default=f"{home_dir}/spparks",
        help="define working dir",
    )
    parser.add_argument(
        "--case_name",
        type=str,
        default="vHpdV_20_0_20_LL_x_10_60_30_7_40_75_35_12_0_1",
        help="define case_name dir",
    )
    args = parser.parse_args()
    main(args)
