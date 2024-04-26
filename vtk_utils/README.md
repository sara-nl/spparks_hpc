# Handling VTK data

Set of functions to handle the `*.vti.i` data generated from SPPARKS. The VTK file format is widely used to describe all types of scientific datasets.

## About the VTK toolkit
Visualization Toolkit (VTK) is an open-source software system for 3D computer graphics, image processing and scientific visualization. For more info, see the official [documentation](https://vtk.org/Wiki/VTK/Tutorials).

For a better understanding on different data types, see [ParaView docs](https://docs.paraview.org/en/latest/UsersGuide/understandingData.html).

## VTK Data format
The easiest way to use VTK in Python is to install it via the Python package manager pip:

`pip install vtk` 

On Snellius, you can load the following module:

`module load VTK/9.2.0.rc2-foss-2022a`

### Performed operations on the vti files

- preprocess raw vtk data to extract 2D or 3D sequences
- read the vtk sequence and convert it to tensor
