# Contrbution to PlantCV-Geospatial

!!! note 
    PlantCV-Geospatial is an add-on package to PlantCV so please first refer to the main package's [contributing guide](https://plantcv.readthedocs.io/en/latest/CONTRIBUTING/) for the majority of the information on what and how to contribute to either project (including but not limited to reporting bugs, requesting new features, add/revise documentation, and adding tutorials). 

## Overview Of What To Contribute to PlantCV-Geospatial vs. Other Packages 

This document aims to give an overview of what to contribute to PlantCV-Geospatial, and guidelines to
decide which repository is the most appropriate place for new features. Please 
[create an issue in GitHub](https://github.com/danforthcenter/plantcv-geospatial/issues) assuming one
does not already exist.

Functions in the Geospatial toolbox are specific to UAV, satellite, and other types of 
georeferenced data. 

## PlantCV-Geospatial Tutorials

Many geospatial workflows require the use of the InteractiveShapes viewer object, which opens a Napari window outside of the jupyter notebook. These functions cannot currently be tested using our Github actions method, but it is useful to test as many steps in tutorials as we can. If you would like to contribute a geospatial tutorial that requires a Napari window, please utilize an existing tutorial (such as `plantcv-geospatial-tutorial-plot-boundaries`) to make the tests file capable of testing InteractiveShapes without needing interaction. A separate tutorial notebook for testing is not needed. 
