# plantcv-geospatial
Geospatial add-on package to PlantCV

[![builds](https://github.com/danforthcenter/plantcv-geospatial/actions/workflows/continuous-integration.yml/badge.svg?branch=main)](https://github.com/danforthcenter/plantcv-geospatial/actions/workflows/continuous-integration.yml)
[![DeepSource](https://app.deepsource.com/gh/danforthcenter/plantcv-geospatial.svg/?label=code+coverage&show_trend=true&token=4ueUDDsEmz3YIs1UPNFPdk4r)](https://app.deepsource.com/gh/danforthcenter/plantcv-geospatial/)
[![DeepSource](https://app.deepsource.com/gh/danforthcenter/plantcv-geospatial.svg/?label=active+issues&show_trend=true&token=4ueUDDsEmz3YIs1UPNFPdk4r)](https://app.deepsource.com/gh/danforthcenter/plantcv-geospatial/)

## Installation

PlantCV-Geospatial requires main PlantCV v5. Follow the [installation instructions](https://docs.plantcv.org/en/stable/installation/) to create a conda environment with recommended dependencies:

```bash
conda create -n plantcv -c conda-forge  jupyterlab ipympl nodejs
```
Then, activate the environment and install main PlantCV version 5 and PlantCV-Geospatial from PyPi:
```bash
conda activate plantcv
pip install 'plantcv==5.0.0rc1' plantcv-geospatial
```


Developers should set up a PlantCV conda environment from source code as normal, then:

```bash
cd plantcv-geospatial
pip install -e . --config-settings editable_mode=strict
```
