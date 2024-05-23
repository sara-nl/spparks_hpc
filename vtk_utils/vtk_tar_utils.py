"""
last modified on Apr 24

Utilities for handling VTK data objects stored in TAR file.
"""

import os
import re
from typing import List, Tuple, Callable, Optional, Dict
import tarfile
import tempfile
import vtk


def count_folders_in_tar(
    tar_path: str, output_dir: str, config_file: str = "metadata"
) -> int:
    """
    Counts number of folders (experiments) in the compressed tar file and saves their names to a config file.

    Parameters:
    - tar_path (str): Path to the tar file.
    - output_dir (str): Directory where the config file will be saved.
    - config_file (str, optional): Name of the config file. Defaults to "config_file.txt".

    Returns:
    - int: Number of directories counted in the tar file.
    """
    os.makedirs(output_dir, exist_ok=True)
    config_path = os.path.join(output_dir, config_file)

    directory_names = []
    n = 0

    try:
        with tarfile.open(tar_path, "r:gz") as tar:
            for member in iter(lambda: tar.next(), None):
                if member.isdir():
                    parts = member.name.split("/")
                    case_name = parts[-1] if parts else member.name
                    directory_names.append(case_name)
                    n += 1

        # Save the directory names to a config file
        with open(config_path, "w") as file:
            for name in directory_names:
                file.write(name + "\t\n")

    except EOFError:
        print("Warning: Reached corrupted section in tar file")

    except tarfile.ReadError:
        print(f"Error reading tar file: {tar_path}")

    return n


def _extract_to_temporary_file(tar_member, tar) -> str:
    """
    Extract a tar file member to a temporary file and return the file path.
    """
    with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
        content = tar.extractfile(tar_member).read()
        tmpfile.write(content)
        tmpfile.flush()  # Ensure all data is written to disk
        return tmpfile.name  # Return the path of the temporary file


def process_file(
    member: tarfile.TarInfo,
    tar: tarfile.TarFile,
    read_instance_function: Callable[[str], vtk.vtkImageData],
) -> Optional[Tuple[int, vtk.vtkImageData]]:
    """
    Process an individual file within a TAR archive.

    This function extracts and processes a single file from the TAR archive,
    specifically a file containing '.vti.' in its name.
    It extracts the index from the file name and reads the corresponding vtkImageData instance.

    Parameters:
    - member: A member of the TAR archive representing a file.
    - tar: The TAR file object being processed.
    - read_instance_function: A function to read vtkImageData from a file path.

    Returns:
      A tuple containing the extracted index and the vtkImageData instance, if the file matches the expected format.
      Returns None if the file does not match the format or if there is no valid index found.
    """
    match = re.search(r"\.vti\.(\d+)", member.name)
    if match:
        n = int(match.group(1))

        temp_file_path = _extract_to_temporary_file(member, tar)
        instance = read_instance_function(temp_file_path)
        return (n, instance)
    else:
        print("No valid index found in file name.")
        return None


def process_directory(
    temporal_sequence: List[Tuple[int, vtk.vtkImageData]],
    all_sample: Dict[int, List[List[vtk.vtkImageData]]],
) -> Tuple[List[vtk.vtkImageData], Dict[int, List[List[vtk.vtkImageData]]]]:
    """
    Process the contents of a directory in a TAR file.

    It appends the current temporal sequence to the correct list in all_sample dictionary,
    updates the count of samples per experiment, and resets the temporal sequence for the next directory.

    Parameters:
    - temporal_sequence: A list of data instances from the current directory.
    - all_sample: A dictionary where each key is a unique count of samples, and the value is a list of lists
      of vtk.vtkImageData instances.
    - num_samples_per_experiment: A list tracking the number of data instances per directory.

    Returns:
      A tuple containing an empty list (reset temporal sequence), the updated all_sample dictionary,
      and the updated num_samples_per_experiment list.
    """
    sample_count = len(temporal_sequence)
    # sort the instances based on time
    sorted_instances = [
        instance for _, instance in sorted(temporal_sequence, key=lambda x: x[0])
    ]

    if sample_count in all_sample:
        all_sample[sample_count].append(sorted_instances)
    else:
        all_sample[sample_count] = [sorted_instances]

    temporal_sequence = []  # reset the buffer
    return temporal_sequence, all_sample
