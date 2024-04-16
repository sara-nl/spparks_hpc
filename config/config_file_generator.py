"""
Last update on Apr 11, 2024

Configuration Generation Script:

- Load parameters from a YAML file.
- Generates configurations and writes them to a config_file.
- the config_file contains all different init conditions to start a Potts kMC simulation on SPPARKS 
    - format per line is 'vHpdV_80_0_20_UR_y_24_70_35_11_48_80_40_16_0_1'
- This script can be run whenever there's a need to update or generate new configurations.

"""

import os
import itertools
from argparse import ArgumentParser
from typing import List, Tuple, Optional
import numpy as np

from concurrent.futures import ProcessPoolExecutor

from potts_param import Potts_Param


def _trans_coord(v, h):
    # v = v*100 # [site/mcs]
    v = [number * 100 for number in v]
    h = h * 1  # [sites]
    return v, h


def _create_config_name(config_map):
    config_name_list = []

    for config in config_map:
        # Convert tuple elements to strings, handle lists inside the tuple separately
        elements = [
            (
                str(item).replace(".", "_")
                if not isinstance(item, list)
                else "_".join(map(lambda x: str(x).replace(".", "_"), item))
            )
            for item in config
        ]

        # Join all elements with underscores and prepend the "vHpdV_"
        config_name = "vHpdV_" + "_".join(elements)
        config_name_list.append(config_name)

    return config_name_list


def create_config_map(
    params: Potts_Param,
    V_laser: List[List[float]],
) -> Tuple[List[Tuple[float, int, str, str, List[float]]], List[str]]:
    """
    Generate a configuration map and associated configuration names based on the provided parameters and V_laser values.
    """

    # coordinate transform
    v_mcs, hatch_site = _trans_coord(params.v_scan, params.hatch)
    all_list = [v_mcs, hatch_site, params.starting_pos, params.heading, V_laser]

    config_map = list(itertools.product(*all_list))
    config_name_list = _create_config_name(config_map)

    return config_map, config_name_list


def _write_chunk(chunk: List[str], output_file: str) -> bool:
    """
    Write a chunk of configuration names to a specified file.

    Parameters:
    - chunk (List[str]): A list of configuration names to be written to the file.
    - output_file (str): The path to the file where the chunk should be written.

    Each configuration name in the chunk is written to a new line in the file,
    followed by a tab character.

    Example:
    If chunk = ["config1", "config2"], the file content will be:
    config1\t
    config2\t

    Note:
    This function will overwrite the content of the file if it already exists.
    """
    try:
        with open(output_file, "w") as file:
            for config_name in chunk:
                file.write(config_name + "\t\n")
        return True
    except IOError:
        return False


def amend_config_file_chunks(
    config_names: List[str], output_dir: str, num_chunks: int = 10
) -> List[Optional[str]]:
    """
    Split a list of configuration names into chunks and write each chunk to a separate file.

    Returns:
    - List[Optional[str]]: A list of file paths where the chunks were successfully written.
      If writing a chunk fails, `None` is included in the list for that chunk.

    This function calculates the chunk size based on the length of `config_names` and the specified `num_chunks`.
    It then splits the `config_names` list into chunks and writes each chunk to a separate file in the `output_dir`.
    The files are named as `config_file_{i}`, where `i` ranges from 1 to `num_chunks`.

    The writing operation is parallelized to improve efficiency. The number of parallel tasks is determined by the
    environment variable `SLURM_CPUS_PER_TASK`, defaulting to 1 if not set.

    Example:
    If config_names = ["config1", "config2", "config3", "config4"] and num_chunks = 2,
    two files will be created in `output_dir`:
    - config_file_1 containing "config1" and "config2"
    - config_file_2 containing "config3" and "config4"

    Note:
    If there's an error writing a chunk, an error message is printed, and the respective position in the returned list
    will contain `None`.
    """
    chunk_size = len(config_names) // num_chunks
    chunks = [
        config_names[i : i + chunk_size]
        for i in range(0, len(config_names), chunk_size)
    ]

    print("num of lines in the chunk: ", len(chunks[0]))

    output_files = [
        os.path.join(output_dir, f"config_file_{i}") for i in range(1, num_chunks + 1)
    ]

    # Write chunks in parallel
    successful_files = []
    cpus_per_task = int(os.environ.get("SLURM_CPUS_PER_TASK", 1))
    with ProcessPoolExecutor(max_workers=cpus_per_task) as executor:
        results = list(executor.map(_write_chunk, chunks, output_files))

    for was_successful, output_file in zip(results, output_files):
        if was_successful:
            successful_files.append(output_file)
        else:
            print(f"Error: Failed to write to {output_file}.")
            successful_files.append(None)

    return successful_files


def amend_config_file(config_names: List[str], output_dir: str) -> Optional[str]:
    """
    Write the provided configuration names to a file in the specified directory.

    Args:
    - config_names (List[str]): A list of configuration names to write.
    - working_dir (str): The directory where the configuration file should be written.

    Returns:
    - str: The path to the written configuration file or None if there was an error.
    """

    config_file = "config_file"
    config_path = os.path.join(output_dir, config_file)

    try:
        with open(config_path, "w") as new_config_file:
            for config_name in config_names:
                new_config_file.write(config_name + "\t\n")

    except IOError as e:
        print(f"Error: Could not amend config file. Reason: {e}")
        return None

    return config_path


def create_HAZ_permutations(params: Potts_Param) -> List[List[int]]:
    """
    Generates a list of valid HAZ (Heat Affected Zone) parameter permutations from a given Potts_Param instance.

    The function extracts relevant HAZ parameters from the Potts_Param object and creates all possible combinations (permutations) of these parameters. A valid combination must satisfy certain conditions where each HAZ dimension parameter (width, tail length, depth, cap height) must be greater than its corresponding base parameter.

    Args:
    - params (Potts_Param): An instance of the Potts_Param class containing simulation parameters.

    Returns:
    - List[List[int]]: A list of all valid parameter combinations. Each combination is a list of integers representing values for spot width, melt tail length, melt depth, cap height, HAZ width, HAZ tail, depth HAZ, cap HAZ, and expansion factor.

    The order of parameters in each combination list is as follows:
    - spot_width
    - melt_tail_length
    - melt_depth
    - cap_height
    - HAZ_width
    - HAZ_tail
    - depth_HAZ
    - cap_HAZ
    - exp_factor

    Example:
    Each list in the output represents a set of parameters that could be used to simulate a specific scenario in a Potts model kinetic Monte Carlo simulation.

    Note:
    The validity of each combination is determined by a set of constraints ensuring that the HAZ parameters are consistently larger than their corresponding base parameters. This reflects the physical expectation that the heat affected zone dimensions should exceed the actual dimensions at which materials are directly affected by the laser in additive manufacturing processes.
    """
    # spot_width melt_tail_length melt_depth cap_height HAZ_width HAZ_tail depth_HAZ cap_HAZ exp_factor
    HAZ_list = [
        params.spot_width,
        params.melt_tail_length,
        params.melt_depth,
        params.cap_height,
        params.HAZ_width,
        params.HAZ_tail,
        params.depth_HAZ,
        params.cap_HAZ,
        params.exp_factor,
    ]

    def _valid_combination(combination):
        return (
            combination[0] < combination[4]  # spot_width < HAZ_width
            and combination[1] < combination[5]  # melt_tail_length < HAZ_tail
            and combination[2] < combination[6]  # melt_depth < depth_HAZ
            and combination[3] < combination[7]  # cap_height < cap_HAZ
        )

    # Generate all permutations of HAZ parameters and filter by validity
    HAZ_map = filter(_valid_combination, itertools.product(*HAZ_list))
    HAZ_map_list = [list(item) for item in HAZ_map]
    return HAZ_map_list


def main(args):
    dirname = os.path.dirname(__file__)
    yaml_file = os.path.join(dirname, args.yaml_file) 
    output_dir = os.path.dirname(dirname)

    os.makedirs(output_dir, exist_ok=True)

    params = Potts_Param(yaml_file)
    V_laser = create_HAZ_permutations(params)

    config_map, config_name_list = create_config_map(params, V_laser)

    print("num possible configurations: ", len(config_name_list))

    # write config file
    path = amend_config_file_chunks(config_name_list, output_dir)
    print("config_file created: ", path)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--yaml_file",
        type=str,
        default=f"param_space.yaml",
        help="yaml file describing the param space",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default=f"./spparks",
        help="define dir where to output config_file",
    )

    args = parser.parse_args()
    main(args)
