## Installation

### Table of contents
1. [Supported platforms and dependencies](#dependencies)
2. [Install via a package manager](#install)
3. [Installing PlantCV-Geospatial for contributors](#contributors)

### Supported platforms and dependencies <a name="dependencies"></a>
- Linux 64-bit, x86 processors
- macOS x86 (Intel) and M (ARM) processors
- Windows 64-bit, x86 processors

First, you must have PlantCV installed, which requires Python (tested with versions 3.11, 3.12, and 3.13) and these [Python packages](https://github.com/danforthcenter/plantcv/blob/main/requirements.txt). Follow one of the methods for [PlantCV Installation](https://plantcv.readthedocs.io/en/latest/installation/) and then continue with the instructions below to add PlantCV-Geospatial to your environment.
Additionally, we recommend installing [JupyterLab](https://jupyter.org/).

### Install via a package manager  <a name="install"></a>

PlantCV-Geospatial requires main PlantCV v5. Follow the [installation instructions](https://docs.plantcv.org/en/stable/installation/) to create a conda environment with recommended dependencies:

```bash
conda create -n plantcv -c conda-forge  jupyterlab ipympl nodejs
```
Then, activate the environment and install main PlantCV version 5 and PlantCV-Geospatial from PyPi:
```bash
conda activate plantcv
pip install 'plantcv==5.0.0rc1' plantcv-geospatial
```


### Installing PlantCV-Geospatial for contributors <a name="contributors"></a>
Before getting started, please read our [contributor guidelines](CONTRIBUTING.md) and [code of conduct](CODE_OF_CONDUCT.md).

You can follow the [PlantCV Installation for Contributor Guide](https://plantcv.readthedocs.io/en/latest/installation/#contributors) and then continue with the instructions below to add PlantCV-Geospatial to 
your development environment.

[PyPi](https://pypi.org/) installation (after [PlantCV Installation](https://plantcv.readthedocs.io/en/latest/installation/#conda)): 

```bash
# Activate the plantcv environment (you will have to do this each time you start a new session)
conda activate plantcv
# Install plantcv-geospatial in editable mode so that it updates as you work on new features/updates
git clone https://github.com/danforthcenter/plantcv-geospatial.git 
cd plantcv-geospatial 
pip install -e .
```
