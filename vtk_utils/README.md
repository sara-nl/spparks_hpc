# Handling VTK data

Set of functions to extract and convert VTK data stored within the compressed TAR file into HDF5 format.

Set of functions to handle the `*.vti.i` data generated from SPPARKS. It provides functionality to process VTK data files, convert them into numpy arrays, and save them as HDF5 datasets.

The script assumes that the VTK files are stored within a compressed TAR file (`.tar.gz`). 

## About the VTK toolkit
The VTK file format is widely used to describe all types of scientific datasets.

The Visualization Toolkit (VTK) is an open-source software system for 3D computer graphics, image processing and scientific visualization. For more info, see the official [documentation](https://vtk.org/Wiki/VTK/Tutorials).

For a better understanding on different data types, see [ParaView docs](https://docs.paraview.org/en/latest/UsersGuide/understandingData.html).

## Data Description 
The data processed by this script originates from simulations conducted using SPPARKS. Each simulation output is encapsulated within a folder, representing an individual experiment. Within each experiment folder, there exists a temporal sequence of `vti.i` files. These files collectively depict the time evolution of the simulated process.

The folder structure of the TAR file typically resembles the following:

```
experiments/
    |-- vHpdV_1/
    |       |-- timestep_0.vti.0
    |       |-- timestep_1.vti.1
    |       |-- ...
    |       |-- timestep_n.vti.n
    |
    |-- vHpdV_2/
    |       |-- timestep_0.vti.0
    |       |-- timestep_1.vti.1
    |       |-- ...
    |       |-- timestep_n.vti.n
    |
    |-- ...
    |
    |-- vHpdV_m/
            |-- timestep_0.vti.0
            |-- timestep_1.vti.1
            |-- ...
            |-- timestep_n.vti.n
```

In this structure:

- Each `vHpdV_i` folder represents a distinct experiment.
- Inside each `vHpdV_i` folder, the `timestep_j.vti.j` files denote the VTK data files capturing the state of the simulation at different time steps.

## Usage of the Python scripts
The Python scripts in this folder assume the experiments `vHpdV_i` are stored within a compressed TAR file (`.tar.gz`).

The script `main_dataformat.py` parses this structure, extracts the VTK data, and organizes it into HDF5 datasets for further analysis or machine learning applications.
### Requirements
Prepare the environment:
```
module load 2022 Python/3.10.4-GCCcore-11.3.0
module load VTK/9.2.0.rc2-foss-2022a
module load h5py/3.7.0-foss-2022a  
module load matplotlib/3.5.2-foss-2022a

source venv/bin/activate
pip install pyvista
```
If you are not on Snellius, you can install them on your system by installing `requirements.txt`.

To run `pyvista` on Snellius, make sure to load the following module:
`module load Xvfb/21.1.3-GCCcore-11.3.0`

Otherwise, be sure to install `libgl1-mesa-glx xvfb` in your package manager. See docs of [PyVista](https://docs.pyvista.org/version/stable/api/utilities/_autosummary/pyvista.start_xvfb.html)

-----


