# SPPARKS on HPC

## Introduction
This repository contains scripts and configurations for running and generating data using the SPPARKS software on a High-Performance Computing (HPC) environment. The scripts have been tested on the [Snellius supercomputer](https://www.surf.nl/en/services/snellius-the-national-supercomputer).

### Table of Contents
1. [About SPPARKS](#about-spparks)
2. [Prerequisites and Environment Setup](#prerequisites-and-environment-setup)
3. [Generate your Configuration File](#generate-your-configuration-file)
4. [Execute SPPARKS](#execute-spparks)
5. [Final Notes](#final-notes)

## About SPPARKS 
SPPARKS is a parallel Monte Carlo code for on-lattice and off-lattice models that includes algorithms for kinetic Monte Carlo (KMC), rejection kinetic Monte Carlo (rKMC), and Metropolis Monte Carlo (MMC). 

It is developed by Sandia Labs, and it is used for modelling additive manufacturing processes via Potts model simulations which evolve microstructure in the presence of a moving laser spot which heats material.

Page and official documentation: https://spparks.github.io/

## Prerequisites and Environment Setup

1. **Install SPPARKS locally**:  

   SPPARKS (and its dependency Stitch) is currently in the process of being integrated into the EasyBuild community GitHub repository (https://github.com/easybuilders). This integration aims to facilitate easier access and management of SPPARKS installations within the scientific and engineering communities.
   
   To load SPPARKS from the proposed changes, run the following commands:
   ```
   module load 2022 eb/4.9.1
   eblocalinstall --from-pr 18049 --include-easyblocks-from-pr 2948 -r --rebuild
   eblocalinstall --from-pr 18050 --include-easyblocks-from-pr 2948 -r --rebuild
   ```
   Now you can load it as a module:
   ```
   module purge
   module load 2022 
   module load spparks/16Jan23-foss-2022a
   ``` 
2. **Activate the Virtual Environment and Install Dependencies**:
   
   Load the Python module and create a virtual environment to manage your Python packages.
   ```
   module load Python/3.10.4-GCCcore-11.3.0
   python -m venv venv
   ```
   After activating the virtual environment, install the required libraries:
   ```
   source venv/bin/activate
   pip install numpy
   pip install PyYAML
   ```
3. **Clone the Repo**
   
   Finally, Get the scripts from this repo.
   ```
   git clone git@github.com:sara-nl/spparks_hpc.git
   cd spparks_hpc
   ```

## Generate your Configuration File
This step involves creating potential configurations from a predefined parameter space which is specified in a YAML file.
You can run the script by submitting a job to the cluster using `sbatch`:
```
sbatch run_config_gen.sh
```
This script will:
- Read the parameters from a YAML file.
- Create possible permutations.
- Write the parameters configurations to single/multiple config files. 

## Execute SPPARKS
Having set the parameter space in proper configurations, these configurations are now executed on SPPARKS to create the dataset.

You can run SPPARKS by submitting a job:
```
sbatch run_spparks.sh
```

The script will:
- Copy relevant files to scratch memory.
- Go over the config file to fetch the correct parameters configuration.
- Amend the spparks input script with the correct parameters values.
- Run SPPARKS with MPI.

Important: remember to copy inside the working folder your own SPPARKS input scripts. Input scripts are named `in.*` and to see how are structured and what commands they contain see [SPPARKS Commands](https://spparks.github.io/doc/Section_commands.html).

## Final Notes
- The scripts are tested on Snellius; Make sure to have enough memory space to generate the data listed in the config file.
- For more information about getting access to Snellius, refer to the [Access to compute services page](https://www.surf.nl/en/access-to-compute-services). 
- For more detailed information about SPPARKS parameters and options, refer to the [Official SPPARKS Documentation](https://spparks.github.io/doc/app_am_ellipsoid.html).
- For information about SPPARKS input scripts, refer to [SPPARKS Commands](https://spparks.github.io/doc/Section_commands.html).
- Parts of the created data (2D slices) have been uploaded to [this Zenodo repository](https://doi.org/10.5281/zenodo.11209659).

This project is a joint effort between SURF and [ESA (TEC Directorate)](https://technology.esa.int/) as part of the digitalization program on advanced manufacturing for space applications.
If you have any question about the code or methods used in this repository you can reach out to monica.rotulo@surf.nl and michael.mallon@esa.int.








