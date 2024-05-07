# Handling VTK data

Set of functions to extract and convert VTK data stored within the compressed TAR file into HDF5 format.

This folder is implemented to handle the `*.vti.i` data generated from SPPARKS. It provides functionality to process VTK data files, convert them into numpy arrays, and save them as HDF5 datasets.

We assume that the VTK files are stored within a compressed TAR file `.tar.gz`.

### Table of Contents
1. [About the VTK toolkit](#about-the-vtk-toolkit)
2. [Data Description](#data-description)
3. [Usage of the Python scripts](#usage-of-the-python-scripts)
4. [Slurm Job Submission Example](#slurm-job-submission-example)
5. [Final Notes](#final-notes)

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

## Slurm Job Submission Example

Below is an example of a Slurm job script for running the scripts on Snellius. Adjust the resource allocations based on the complexity of your tasks and available resources.

```
#!/bin/bash
#SBATCH --job-name=create_dataset
#SBATCH --nodes=1
#SBATCH --time=1-00:00:00
#SBATCH --partition=gpu     # 'himem_8tb' for the high memory node
#SBATCH --exclusive

# Activate environment and load necessary modules
source venv/bin/activate
module load 2022 
module load VTK/9.2.0.rc2-foss-2022a h5py/3.7.0-foss-2022a Xvfb/21.1.3-GCCcore-11.3.0 matplotlib/3.5.2-foss-2022a

SPPARKS="${HOME}/spparks"
EXPERIMENTS="${SPPARKS}/2023-10-20_11-43-44_4220682"
PERSONALSPACE="${HOME}/spparks"     # insert your personal space

EXPERIMENT_NUM=1
TAR="${PERSONALSPACE}/exp_${EXPERIMENT_NUM}.tar.gz"

python main_dataformat.py --tar_path ${TAR} --output_path ${PERSONALSPACE} --output_name "exp_${EXPERIMENT_NUM}"

```

## Final Notes
- The scripts are tested on Snellius; Make sure to have enough memory to process the VTK data.
- The scripts can be easily modified to support and process 3D Lattice data.
- Further documentation on how to process VTK format with Python: [Kitware Docs](https://www.kitware.com/easy-data-conversion-to-vtk-with-python/)
_ For any questions, you can reach out to monica.rotulo@surf.nl.

