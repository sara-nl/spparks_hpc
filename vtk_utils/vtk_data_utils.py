"""
last modified on Apr 24

Utilities for handling VTK data objects
"""

import os
from typing import List, Tuple
import numpy as np
from argparse import ArgumentParser
import pyvista as pv

import h5py
import vtk
from vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk

CELL_DATA = "Spin"  # Used specifically for the Scalars attribute in CellData


"""Collection of methods for reading the "subfolder/*.vti.*" generated from SPPARKS"""
"""generate hdf5 dataset from all subfolders"""
"""also revert vti back from hdf5 as test (and for future use)"""


def read_vtk_instance(filename: str) -> vtk.vtkImageData:
    """Read single vti.n file"""
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(filename)
    reader.Update()
    vtk_data_object = reader.GetOutput()

    return vtk_data_object


def extract_top_2D_slice_with_voi(
    vtk_data_object: vtk.vtkImageData,
) -> vtk.vtkImageData:
    """
    Extract the top 2D slice (highest Z-index) from the 3D vtkImageData object using vtkExtractVOI.

    Parameters:
    vtk_data_object (vtk.vtkImageData): The 3D image data to slice.

    Returns:
    vtk.vtkImageData: The extracted top 2D image slice.
    """
    # Get dimensions of the input data
    dims = vtk_data_object.GetDimensions()

    # Extract the VOI for the top slice
    extract_voi = vtk.vtkExtractVOI()
    extract_voi.SetInputData(vtk_data_object)
    extract_voi.SetVOI(0, dims[0] - 1, 0, dims[1] - 1, dims[2] - 1, dims[2] - 1)
    extract_voi.Update()

    return extract_voi.GetOutput()


def convert_vtk_instance_to_numpy(
    vtk_data_object: vtk.vtkImageData,
    array_name: str = CELL_DATA,
    slicing: bool = False,
) -> np.ndarray:
    """
    Convert a vtkImageData instance (vti.n) to a NumPy array, handling both 2D and 3D data.

    Parameters:
    - vtk_data_object (vtk.vtkImageData): The vtkImageData object to convert.
    - array_name (str, optional): The name of the array to extract from the vtkDataObject. Defaults to "Spin".
    - slicing (bool, optional): If True, handles 2D data by removing singleton dimensions. Defaults to False.

    Returns:
    - np.ndarray: A NumPy array containing the data from the vtkImageData object.
    """

    # Decide between cell data and point data
    if vtk_data_object.GetCellData().GetNumberOfArrays() > 0:
        data = vtk_data_object.GetCellData()
    else:
        data = vtk_data_object.GetPointData()

    # Use the specified array or the first available array
    if array_name:
        vtk_array = data.GetArray(array_name)
    else:
        vtk_array = data.GetArray(0)

    if vtk_array is None:
        raise ValueError("No suitable data array found in vtkImageData.")

    # get additional info (not used for now)
    spacing = vtk_data_object.GetSpacing()
    range_min, range_max = vtk_array.GetRange()  # useful for normalize my data
    num_components = vtk_array.GetNumberOfComponents()

    np_array = vtk_to_numpy(vtk_array)

    # Subtract 1 to get the correct dimensions for cell data
    dims = vtk_data_object.GetDimensions()

    # Handle 3D cell data
    if len(dims) == 3 and data == vtk_data_object.GetCellData():
        dims = (dims[0] - 1, dims[1] - 1, dims[2] - 1)

    # Handle 2D data (slices)
    if slicing:
        dims = tuple(d for d in dims if d > 1)

    np_array = np_array.reshape(dims)

    return np_array


def read_vtk_sample(path: str) -> List[np.ndarray]:
    """We are inside a vHpdV_ folder (that's my sample): read the temporal sequence"""
    """Files stored in file sys"""
    # Iterate over the range of numbers from vti.0 to vti.N
    temporal_sample = []
    n = 0
    while True:
        file_path = os.path.join(path, f"IN1003d.vti.{n}")
        if not os.path.isfile(file_path):
            break

        instance = read_vtk_instance(file_path)
        temporal_sample.append(instance)

        n += 1

    return temporal_sample


def read_vtk_from_path(data_path: str, config_file: str) -> List[List[np.ndarray]]:
    """
    Read the samples path from config file

    the np.ndarray shape is (100,100,50)
    """

    data_list = []
    with open(config_file, "r") as file:
        for line in file:
            subfolder = line.strip()
            path = os.path.join(data_path, subfolder)

            sample = read_vtk_sample(path)  # sample[0].shape = (100,100,50)

            data_list.append(sample)

    # print(len(data_list[0]))  # single sample

    return data_list
