"""
Script for reading the vti data from h5 data format
Last modified: 14 May 2024
"""
import os
import re
from typing import List, Tuple
import numpy as np
from argparse import ArgumentParser

import h5py
import vtk
from vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk

from visualization_utils import render_2D_from_numpy, numpy_to_vtk_file


class H5_Handler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.experiments_length = self.extract_length(file_path)

    def extract_length(self, filename):
        # Use a regular expression to find 'len' followed by an underscore and one or more digits
        match = re.search(r"len_(\d+)", self.file_path)
        if match:
            return int(
                match.group(1)
            )  # Convert the matched string (digits only) to an integer
        else:
            return None  # Return None if no match is found

    def load_experiment(self, video_idx):
        """
        Read and return a range of images from the HDF5 file.

        video_index (int): Index of the video for which frames are to be loaded (0-indexed).
        return:numpy.ndarray: Array of frames for the specified video.
        """
        start_idx = video_idx * self.experiments_length
        end_idx = start_idx + self.experiments_length

        with h5py.File(self.file_path, "r") as file:
            images = file["images"][start_idx:end_idx]
        return images

    def get_total_frames(self):
        """
        Get the total number of frames (images) in the HDF5 file.

        return: int, the total number of images in the file.
        """
        with h5py.File(self.file_path, "r") as file:
            num_frames = len(file["images"])
        return num_frames

    def get_total_experiments(self):
        """
        Get the total number of experiments (temporal sequence of images) in the HDF5 file.

        return: int, the total number of experiments stored in the file.
        """
        with h5py.File(self.file_path, "r") as file:
            num_frames = len(file["images"])

        return num_frames // self.experiments_length


def visualize_all_sequence_from_numpy(
    sequence: List[np.ndarray], filename: str = "instance"
) -> None:
    """
    Processes a sequence of frames, rendering each as an image.

    Args:
    sequence (List[np.ndarray]): A list of numpy arrays representing image data.
    """
    for i, frame in enumerate(sequence):
        if isinstance(frame, np.ndarray):
            render_2D_from_numpy(frame, filename=f"{filename}_{i}.png")
        else:
            print(f"Skipping index {i}: not a numpy array")


def main(args):
    data_path = args.data_path
    experiment = args.experiment

    data_handler = H5_Handler(os.path.join(data_path, experiment))

    video_idx = 0  # For example, load frames from video 2 (index 1)
    sequence_0 = data_handler.load_experiment(video_idx)

    # now you can visualize it or
    visualize_all_sequence_from_numpy(sequence_0, "image")

    for i, frame in enumerate(sequence_0):
        numpy_to_vtk_file(frame, f"process_2d.vti.{i}")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--data_path", type=str, default="/projects/1/monicar/")
    parser.add_argument(
        "--experiment",
        type=str,
        default="exp_6_len_28_2D.h5",
    )

    args = parser.parse_args()
    main(args)
