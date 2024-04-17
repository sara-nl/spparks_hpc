# SPPARKS on Snellius HPC

## Introduction
This repository contains scripts and configurations for running and generating data using the SPPARKS software on the Snellius High-Performance Computing (HPC) environment. 

### Table of Contents
1. [About SPPARKS](#about-spparks)
2. [Prerequisites and Environment Setup](#prerequisities-and-environment-setup)
3. [Preparing your Configuration Parameters](#preparing-your-configuration-parameters)
4. [Running SPPARKS](#running-spparks)
5. [Slurm Job Submission Example](#slurm-job-submission-example)

## About SPPARKS 
SPPARKS is a parallel Monte Carlo code for on-lattice and off-lattice models that includes algorithms for kinetic Monte Carlo (KMC), rejection kinetic Monte Carlo (rKMC), and Metropolis Monte Carlo (MMC). 

It is developed by Sandia Labs, and it is used for modelling additive manufacturing processes via Potts model simulations which evolve microstructure in the presence of a moving laser spot which heats material.

Page and official documentation: https://spparks.github.io/

## Prerequisites and Environment Setup
### Python Virtual Environment and Dependencies
1. **Create a Directory for SPPARKS**:
   ```
   mkdir spparks
   ```
2. **Load SPPARKS as a module**:
   SPPARKS (and its dependency Stitch) is currently in the process of being integrated into the EasyBuild community GitHub repository (https://github.com/easybuilders). This integration aims to facilitate easier access and management of SPPARKS installations within the scientific and engineering communities.
   To load SPPARKS from the proposed changes, run the following commands:
   ```
   eblocalinstall --from-pr 18049 --include-easyblocks-from-pr 2948 -r --rebuild
   eblocalinstall --from-pr 18050 --include-easyblocks-from-pr 2948 -r --rebuild
   ```
   Now you can load it as a module:
   ```
   module load spparks/16Jan23-foss-2022a
   ``` 
4. **Load Python module**:
   Load the Python module and create a virtual environment to manage your Python packages.
   ```
   module load 2022
   module load Python/3.10.4-GCCcore-11.3.0
   python -m venv venv
   ```
5. **Activate the Virtual Environment and Install Dependencies**:
   After activating the virtual environment, install the required libraries.
   ```
   module purge
   source venv/bin/activate
   pip install numpy
   pip install PyYAML
   ```
   Get the scripts from this repo.
   ```
   git clone https://github.com/sara-nl/SPPARKS_Snellius.git
   cd SPPARKS_Snellius
   ```

## Preparing your Configuration Parameters

The dataset creation pipeline consists of two main steps:
1. Generating possible configurations from a defined parameter space.
2. Executing these configurations on SPPARKS to create the dataset.

## Running SPPARKS

## Slurm Job Submission Example





